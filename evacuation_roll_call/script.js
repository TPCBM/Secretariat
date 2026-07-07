(function () {
  'use strict';

  // ========== 替換為你的 GAS 網頁應用程式部署網址 ==========
  // 請確認網址結尾是 /exec
  const API_URL = 'https://script.google.com/macros/s/你的_DEPLOY_ID/exec';

  // ---------- 改用 fetch 呼叫 GAS API ----------
  function apiLogin(code) {
    return fetch(`${API_URL}?action=login&code=${encodeURIComponent(code)}`)
      .then(function(res) { return res.json(); });
  }

  function apiGetRoster(code, floor) {
    return fetch(`${API_URL}?action=getRoster&code=${encodeURIComponent(code)}&floor=${encodeURIComponent(floor)}`)
      .then(function(res) { return res.json(); });
  }

  function apiSubmitChanges(code, floor, changes) {
    const payload = {
      action: 'submitChanges',
      code: code,
      floor: floor,
      changes: changes
    };

    return fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'text/plain;charset=utf-8'
      },
      body: JSON.stringify(payload)
    }).then(function(res) { return res.json(); });
  }

  // ---------- 狀態 ----------
  var state = {
    leader: null,   // { code, name, floors: [...] }
    floor: null,
    people: [],     // [{ code, name, unit, group, checked }] —— checked 一律代表「畫面上顯示的狀態」
    pending: {},    // 分組頁籤裡尚未按「送出更新」的暫存變更： { 姓名代號: 期望的新狀態(boolean) }
    tab: 'absent',
    query: '',
  };

  // ---------- 背景同步佇列（樂觀更新的核心）----------
  var syncQueue = [];
  var syncBusy = false;
  var hasSyncError = false;

  function effectiveChecked(p) {
    return Object.prototype.hasOwnProperty.call(state.pending, p.code) ? state.pending[p.code] : p.checked;
  }
  function rowStateClass(p) {
    var base = p.checked, eff = effectiveChecked(p);
    if (!base && !eff) return 'state-off';
    if (!base && eff) return 'state-off-pending';
    if (base && eff) return 'state-on';
    return 'state-on-pending';
  }
  function escapeHtml(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // ---------- DOM 快取 ----------
  var el = {};
  function cacheEl() {
    ['view-login', 'view-roster', 'login-form', 'login-code', 'login-btn', 'login-error',
      'floor-switch', 'sync-indicator', 'tally-present', 'tally-total', 'tally-floor-name',
      'search-input', 'segmented', 'roster-list', 'action-bar', 'pending-label', 'btn-submit',
      'btn-logout', 'count-absent', 'count-present', 'toast', 'overlay']
      .forEach(function (id) { el[id] = document.getElementById(id); });
  }

  function showView(name) {
    el['view-login'].hidden = name !== 'login';
    el['view-roster'].hidden = name !== 'roster';
  }
  function setBusy(on) { el.overlay.hidden = !on; }
  var toastTimer = null;
  function showToast(msg, isError) {
    el.toast.textContent = msg;
    el.toast.className = 'toast' + (isError ? ' error' : '');
    el.toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.toast.hidden = true; }, 2600);
  }

  function hasUnsyncedWork() {
    return Object.keys(state.pending).length > 0 || syncQueue.length > 0;
  }

  // ---------- 登入 ----------
  function bindLogin() {
    el['login-form'].addEventListener('submit', function (e) {
      e.preventDefault();
      var code = el['login-code'].value.trim();
      if (!code) return;
      el['login-error'].hidden = true;
      el['login-btn'].disabled = true;
      el['login-btn'].textContent = '登入中…';
      apiLogin(code).then(function (res) {
        el['login-btn'].disabled = false;
        el['login-btn'].textContent = '開始點名';
        if (!res.ok) {
          el['login-error'].textContent = res.message;
          el['login-error'].hidden = false;
          return;
        }
        state.leader = { code: res.code, name: res.name, floors: res.floors };
        renderFloorSwitch();
        loadRoster(res.floors[0]);
      }).catch(function (err) {
        el['login-btn'].disabled = false;
        el['login-btn'].textContent = '開始點名';
        el['login-error'].textContent = '系統發生錯誤：' + (err && err.message ? err.message : err);
        el['login-error'].hidden = false;
      });
    });

    el['btn-logout'].addEventListener('click', function () {
      if (hasUnsyncedWork()) {
        if (!confirm('尚有點名資料還在背景同步中，確定要離開嗎？')) return;
      }
      state = { leader: null, floor: null, people: [], pending: {}, tab: 'absent', query: '' };
      syncQueue = []; syncBusy = false; hasSyncError = false;
      el['login-code'].value = '';
      el['search-input'].value = '';
      showView('login');
    });
  }

  function renderFloorSwitch() {
    var floors = state.leader.floors;
    if (floors.length <= 1) {
      el['floor-switch'].innerHTML = '';
      return;
    }
    el['floor-switch'].innerHTML = floors.map(function (f) {
      var active = f === state.floor ? ' active' : '';
      return '<button class="' + active.trim() + '" data-floor="' + escapeHtml(f) + '">' + escapeHtml(f) + '</button>';
    }).join('');
  }
  function bindFloorSwitch() {
    el['floor-switch'].addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-floor]');
      if (!btn) return;
      var floor = btn.dataset.floor;
      if (floor === state.floor) return;
      if (Object.keys(state.pending).length > 0 && !confirm('切換樓層將捨棄尚未送出的暫存變更，確定要切換嗎？')) return;
      loadRoster(floor);
    });
  }

  // ---------- 載入點名名單 ----------
  function loadRoster(floor) {
    setBusy(true);
    apiGetRoster(state.leader.code, floor).then(function (res) {
      setBusy(false);
      if (!res.ok) { showToast(res.message, true); return; }
      state.floor = floor;
      state.people = res.people;
      state.pending = {};
      state.tab = 'absent';
      state.query = '';
      el['search-input'].value = '';
      document.querySelectorAll('.seg-btn').forEach(function (b) { b.classList.toggle('active', b.dataset.tab === 'absent'); });
      el['tally-floor-name'].textContent = floor;
      renderFloorSwitch();
      showView('roster');
      render();
    }).catch(function (err) {
      setBusy(false);
      showToast('載入失敗：' + (err && err.message ? err.message : err), true);
    });
  }

  // ---------- 搜尋 ----------
  function bindSearch() {
    el['search-input'].addEventListener('input', function () {
      state.query = el['search-input'].value;
      renderList();
    });
  }

  // ---------- 點名列表互動 ----------
  function bindSegmented() {
    el.segmented.addEventListener('click', function (e) {
      var btn = e.target.closest('.seg-btn');
      if (!btn) return;
      state.tab = btn.dataset.tab;
      document.querySelectorAll('.seg-btn').forEach(function (b) { b.classList.toggle('active', b === btn); });
      renderList();
    });
  }

  function bindRosterList() {
    el['roster-list'].addEventListener('click', function (e) {
      var batchBtn = e.target.closest('.btn-batch');
      if (batchBtn) { batchToggleGroup(batchBtn.dataset.key); return; }
      var row = e.target.closest('.person-row');
      if (row) togglePending(row.dataset.code);
    });
  }

  function togglePending(code) {
    var p = state.people.find(function (x) { return x.code === code; });
    if (!p) return;
    var next = !effectiveChecked(p);
    if (next === p.checked) delete state.pending[code];
    else state.pending[code] = next;
    render();
  }

  function batchToggleGroup(key) {
    var target = state.tab === 'absent';
    var tabBaseMatch = state.tab === 'present';
    var q = state.query.trim().toLowerCase();
    state.people.forEach(function (p) {
      if ((p.unit + '｜' + p.group) !== key) return;
      if (p.checked !== tabBaseMatch) return;
      if (q && p.name.toLowerCase().indexOf(q) === -1 && p.code.toLowerCase().indexOf(q) === -1) return;
      if (effectiveChecked(p) === target) return;
      if (target === p.checked) delete state.pending[p.code];
      else state.pending[p.code] = target;
    });
    render();
  }

  function bindSubmit() {
    el['btn-submit'].addEventListener('click', function () {
      var changes = state.pending;
      var count = Object.keys(changes).length;
      if (count === 0) return;
      applyOptimistic_(changes);
      state.pending = {};
      render();
      showToast('已更新 ' + count + ' 人');
      enqueueSubmit(changes);
    });
  }

  function applyOptimistic_(changes) {
    Object.keys(changes).forEach(function (code) {
      var p = state.people.find(function (x) { return x.code === code; });
      if (p) p.checked = !!changes[code];
    });
  }

  // ---------- 背景同步佇列 ----------
  function enqueueSubmit(changes) {
    if (!changes || Object.keys(changes).length === 0) return;
    syncQueue.push({
      leaderCode: state.leader.code,
      floor: state.floor,
      changes: changes,
      retries: 0,
    });
    pumpQueue();
  }

  function pumpQueue() {
    if (syncBusy) return;
    if (syncQueue.length === 0) {
      if (!hasSyncError) setSyncStatus('idle');
      return;
    }
    syncBusy = true;
    setSyncStatus('syncing');
    var batch = syncQueue[0];
    apiSubmitChanges(batch.leaderCode, batch.floor, batch.changes).then(function (res) {
      syncBusy = false;
      syncQueue.shift();
      if (!res.ok) {
        hasSyncError = true;
        setSyncStatus('error', res.message);
        return; 
      }
      hasSyncError = false;
      pumpQueue();
    }).catch(function (err) {
      syncBusy = false;
      batch.retries += 1;
      if (batch.retries <= 2) {
        setSyncStatus('syncing');
        setTimeout(pumpQueue, 1200 * batch.retries); 
      } else {
        hasSyncError = true;
        setSyncStatus('error', '網路連線異常，尚有點名資料未同步成功');
      }
    });
  }

  function setSyncStatus(mode, message) {
    var ind = el['sync-indicator'];
    if (mode === 'idle') {
      ind.hidden = true;
      ind.className = 'sync-indicator';
      return;
    }
    ind.hidden = false;
    if (mode === 'syncing') {
      ind.className = 'sync-indicator syncing';
      ind.textContent = '● 同步中';
      ind.title = '';
    } else if (mode === 'error') {
      ind.className = 'sync-indicator error';
      ind.textContent = '⚠ 尚有 ' + (syncQueue.length + 1) + ' 筆未同步，點此重試';
      ind.title = message || '';
    }
  }

  function bindSyncIndicatorRetry() {
    el['sync-indicator'].addEventListener('click', function () {
      if (!el['sync-indicator'].classList.contains('error')) return;
      hasSyncError = false;
      pumpQueue();
    });
  }

  // ---------- 渲染 ----------
  function groupPeople(list) {
    var order = [];
    var map = {};
    list.forEach(function (p) {
      var key = p.unit + '｜' + p.group;
      if (!map[key]) { map[key] = { key: key, unit: p.unit, group: p.group, items: [] }; order.push(key); }
      map[key].items.push(p);
    });
    return order.map(function (k) { return map[k]; });
  }

  function render() {
    renderTally();
    renderCounts();
    renderList();
    renderActionBar();
  }

  function renderTally() {
    var total = state.people.length;
    var present = state.people.filter(function (p) { return effectiveChecked(p); }).length;
    el['tally-present'].textContent = present;
    el['tally-total'].textContent = total;
  }

  function renderCounts() {
    var absent = state.people.filter(function (p) { return !p.checked; }).length;
    var present = state.people.length - absent;
    el['count-absent'].textContent = absent;
    el['count-present'].textContent = present;
  }

  function renderList() {
    var q = state.query.trim().toLowerCase();
    var base = state.people.filter(function (p) {
      return state.tab === 'absent' ? !p.checked : p.checked;
    });
    var filtered = q
      ? base.filter(function (p) {
          return p.name.toLowerCase().indexOf(q) !== -1 || p.code.toLowerCase().indexOf(q) !== -1;
        })
      : base;

    if (filtered.length === 0) {
      var msg;
      if (q) {
        msg = '在「' + (state.tab === 'absent' ? '未到名單' : '已到名單') + '」裡找不到符合「' + escapeHtml(state.query.trim()) + '」的人員';
      } else {
        msg = state.tab === 'absent' ? '🎉 全部人員都已完成點名' : '目前還沒有人完成點名';
      }
      el['roster-list'].innerHTML = '<div class="empty-state">' + msg + '</div>';
      return;
    }

    var groups = groupPeople(filtered);
    var batchLabel = state.tab === 'absent' ? '本組全部點到' : '本組全部取消';

    el['roster-list'].innerHTML = groups.map(function (g) {
      var doneInGroup = g.items.filter(function (p) { return effectiveChecked(p); }).length;
      var rows = g.items.map(function (p) {
        return '<li class="person-row ' + rowStateClass(p) + '" data-code="' + escapeHtml(p.code) + '">' +
          '<span class="check-box"></span>' +
          '<span class="person-name">' + escapeHtml(p.name) + '</span>' +
          '<span class="person-code">' + escapeHtml(p.code) + '</span>' +
          '</li>';
      }).join('');
      return '<div class="group-card">' +
        '<div class="group-head">' +
        '<span class="group-name">' + escapeHtml(g.unit) + '－' + escapeHtml(g.group) + '</span>' +
        '<span class="group-count">' + doneInGroup + '/' + g.items.length + '</span>' +
        '<button class="btn-batch" data-key="' + escapeHtml(g.key) + '">' + batchLabel + '</button>' +
        '</div>' +
        '<ul class="person-list">' + rows + '</ul>' +
        '</div>';
    }).join('');
  }

  function renderActionBar() {
    var count = Object.keys(state.pending).length;
    el['action-bar'].hidden = count === 0;
    el['pending-label'].textContent = '已變更 ' + count + ' 人';
  }

  document.addEventListener('DOMContentLoaded', function () {
    cacheEl();
    bindLogin();
    bindFloorSwitch();
    bindSearch();
    bindSegmented();
    bindRosterList();
    bindSubmit();
    bindSyncIndicatorRetry();
    showView('login');

    window.addEventListener('beforeunload', function (e) {
      if (hasUnsyncedWork()) {
        e.preventDefault();
        e.returnValue = '';
      }
    });
  });
})();
