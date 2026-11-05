"""Read-only content for the original client's summon drop-rate WebView."""
from functools import lru_cache
from html import escape
import json
from pathlib import Path

from data_paths import TEXT_DIR


@lru_cache(maxsize=1)
def _item_names():
    names = {}
    for filename in ('F_TEXT_ITEM_NAME.ndjson', 'F_TEXT_IMPORTANT_ITEM_NAME.ndjson'):
        with (Path(TEXT_DIR) / filename).open(encoding='utf-8') as source:
            for line in source:
                row = json.loads(line)
                values = row.get('v', [])
                if values:
                    names[row['key'].rsplit('_', 1)[-1]] = values[0]
    return names


def reward_name(reward):
    from ffbe_gacha import unit_name
    if reward.get('display_name'):
        return str(reward['display_name'])
    if int(reward['kind']) in (30, 31, 50):
        return {30: 'Gil', 31: 'Friend Points', 50: 'Lapis'}[int(reward['kind'])]
    if int(reward['kind']) == 10:
        name = unit_name(reward['id']) or 'Unit ' + str(reward['id'])
        points = reward.get('affinity_points', [])
        if len(points) == 2 and any(str(point).isdigit() and int(point) for point in points):
            name += ' (ALL ' + str(max(int(p) if str(p).isdigit() else 0 for p in points) / 10).rstrip('0').rstrip('.') + '%)'
        return name
    return _item_names().get(str(reward['id']), 'Item ' + str(reward['id']))


def _table(pool, mixed=False):
    from ffbe_gacha import unit_name
    total = sum(max(0, float(row.get('rate', 0))) for row in pool)
    if not total:
        return '<p>No eligible rewards.</p>'
    rows = []
    for row in sorted(pool, key=lambda r: -float(r.get('rate', 0))):
        name = reward_name(row) if mixed else unit_name(row['unit_id'])
        count = int(row.get('count', 1))
        chance = max(0, float(row.get('rate', 0))) * 100 / total
        rows.append('<tr><td>%s%s</td><td>%.6f%%</td></tr>' % (
            escape(name), (' x' + str(count)) if count != 1 else '', chance))
    return '<table><thead><tr><th>Reward</th><th>Chance per draw</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'


def selectable_units():
    try:
        from player_state import unit_roots_by_rarity, named_unit_ids
        from ffbe_gacha import unit_name
        roots = unit_roots_by_rarity()
        named = named_unit_ids()
        units = []
        seen = set()
        from player_state import unit_mst
        for r_str, label in (('7', 'NV'), ('5', '5★')):
            for uid in roots.get(r_str, []):
                uid_str = str(uid)
                if uid_str.startswith('9') or uid_str in seen:
                    continue
                # For NV units, the summonable base form has form index '0' before rarity '7' (e.g. ...07)
                # Transformed Brave Shift forms end in 17, 27, etc. and are battle stances, not summonable units.
                if r_str == '7' and len(uid_str) >= 2 and uid_str[-2] != '0':
                    continue
                if named and uid_str not in named:
                    continue
                name = unit_name(uid_str)
                if not name or name.lower().startswith('dummy') or name.lower().startswith('test'):
                    continue
                seen.add(uid_str)
                mst = unit_mst(uid_str) or {}
                is_nv_plus = (r_str == '7' and str(mst.get('5Mgpv8hJ')) == '2')
                u_label = 'NV+' if is_nv_plus else label
                u_rnum = 8 if is_nv_plus else int(r_str)
                units.append({
                    'id': uid_str,
                    'name': name,
                    'rarity': u_label,
                    'rarity_num': u_rnum
                })
        if len(units) < 20:
            import json
            named_json_path = Path(__file__).with_name('gacha_named.json')
            if named_json_path.exists():
                with open(named_json_path, encoding='utf-8') as f:
                    nd = json.load(f)
                u_banner = next((b for b in nd.get('banners', []) if b.get('id') == '9200005'), None)
                if u_banner:
                    t7 = next((t for t in (u_banner.get('pool') or {}).get('tiers', []) if t.get('rarity') == 7), None)
                    for uid in (t7.get('units') or []):
                        uid_str = str(uid)
                        if len(uid_str) >= 2 and uid_str[-2] != '0':
                            continue
                        if uid_str not in seen:
                            name = unit_name(uid_str) or f"Neo Vision {uid_str}"
                            seen.add(uid_str)
                            mst = unit_mst(uid_str) or {}
                            is_nv_plus = (str(mst.get('5Mgpv8hJ')) == '2')
                            units.append({'id': uid_str, 'name': name, 'rarity': 'NV+' if is_nv_plus else 'NV', 'rarity_num': 8 if is_nv_plus else 7})
        units.sort(key=lambda u: (0 if u['rarity'] == 'NV+' else (1 if u['rarity'] == 'NV' else 2), u['name'].lower()))
        return units
    except Exception:
        return [
            {'id': '100045107', 'name': 'Azure and Crimson Blades Rhus', 'rarity': 'NV', 'rarity_num': 7},
            {'id': '100044807', 'name': 'Crimson Knight Rain', 'rarity': 'NV', 'rarity_num': 7},
            {'id': '100044907', 'name': 'Azure Knight Lasswell', 'rarity': 'NV', 'rarity_num': 7},
            {'id': '100045007', 'name': 'Hero Resurrected Taivas', 'rarity': 'NV', 'rarity_num': 7},
            {'id': '100014307', 'name': 'Sephiroth', 'rarity': 'NV', 'rarity_num': 7},
            {'id': '100013007', 'name': 'Cloud', 'rarity': 'NV', 'rarity_num': 7},
            {'id': '100010007', 'name': 'Rain -Neo Vision-', 'rarity': 'NV', 'rarity_num': 7},
            {'id': '100010107', 'name': 'Lasswell -Neo Vision-', 'rarity': 'NV', 'rarity_num': 7},
            {'id': '100010207', 'name': 'Fina -Neo Vision-', 'rarity': 'NV', 'rarity_num': 7},
            {'id': '100010005', 'name': 'Awakened Rain', 'rarity': '5★', 'rarity_num': 5},
            {'id': '100010105', 'name': 'Pyro Glacial Lasswell', 'rarity': '5★', 'rarity_num': 5},
            {'id': '100010205', 'name': 'Lotus Mage Fina', 'rarity': '5★', 'rarity_num': 5},
        ]


def _custom_stepup_picker_html(current_pool):
    from ffbe_gacha import unit_name
    pool_ids = [str(x) for x in (current_pool or [])]
    units = selectable_units()
    units_json = json.dumps(units)
    pool_json = json.dumps(pool_ids)

    locked_alert_style = "" if not pool_ids else 'style="display:none;"'

    return f'''
<div class="custom-stepup-card">
    <div class="stepup-header-badge">UNITED FORCES STEP-UP</div>
    <h2 style="margin: 6px 0 8px 0; color: #ffe398; font-size: 20px;">Custom Rate-Up Pool Selector</h2>
    <p style="margin: 0 0 14px 0; font-size: 14px; line-height: 1.45; color: #cbe0fc;">
        Add any <strong>Neo Vision (NV)</strong> or <strong>5★ Base</strong> characters below to build your custom rate-up pool!
        Selected units share a massive <strong>25% rate-up share</strong> on their tier across all 6 steps, and
        <strong style="color: #ffd700;">Step 6 guarantees at least one unit from your custom pool</strong>!
    </p>

    <div id="poolLockedAlert" class="locked-alert" {locked_alert_style} style="background: rgba(230, 57, 70, 0.2); border: 1px solid #ff4d6d; border-radius: 8px; padding: 10px 14px; margin-bottom: 14px; color: #ffb3c1; font-size: 13px; line-height: 1.45;">
        🔒 <strong>Summon Button Locked:</strong> You currently have no rate-up units selected. Tap <strong>"+ Add to Pool"</strong> on at least one character below to unlock the banner for summoning!
    </div>

    <div class="active-pool-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 1px; color: #9bbcdb; font-weight: bold;">
                Active Rate-Up Pool (<span id="poolCount">{len(pool_ids)}</span> unit(s)):
            </div>
            <button type="button" class="clear-pool-btn" id="clearPoolBtn" onclick="clearPool()" {'style="display:none"' if not pool_ids else ''}>Clear All</button>
        </div>
        <div id="activePoolPills" class="active-pool-pills"></div>
    </div>

    <div class="filter-toolbar">
        <input type="text" id="unitSearchInput" placeholder="🔍 Search character by name or ID..." oninput="applyUnitFilter()">
        <div class="filter-pills">
            <button type="button" class="pill-btn active" id="pillAll" onclick="selectRarityFilter('all')">All ({len(units)})</button>
            <button type="button" class="pill-btn" id="pillNVPlus" onclick="selectRarityFilter('NV+')">NV+ ({len([u for u in units if u['rarity'] == 'NV+'])})</button>
            <button type="button" class="pill-btn" id="pillNV" onclick="selectRarityFilter('NV')">NV ({len([u for u in units if u['rarity'] == 'NV'])})</button>
            <button type="button" class="pill-btn" id="pill5" onclick="selectRarityFilter('5★')">5★ ({len([u for u in units if u['rarity'] == '5★'])})</button>
        </div>
    </div>

    <div class="unit-picker-scroll">
        <div id="unitResultsList" class="unit-results-list"></div>
    </div>
</div>

<div id="toastMessage" class="toast-popup"></div>

<script>
(function() {{
    const allUnits = {units_json};
    const unitMap = {{}};
    allUnits.forEach(u => {{ unitMap[u.id] = u; }});
    let activePool = new Set({pool_json});
    let activeRarity = 'all';

    function showToast(msg) {{
        const t = document.getElementById('toastMessage');
        if (!t) return;
        t.textContent = msg;
        t.classList.add('show');
        setTimeout(() => t.classList.remove('show'), 2000);
    }}

    function renderActivePool() {{
        const container = document.getElementById('activePoolPills');
        const countSpan = document.getElementById('poolCount');
        const clearBtn = document.getElementById('clearPoolBtn');
        const lockAlert = document.getElementById('poolLockedAlert');
        if (!container) return;
        countSpan.textContent = activePool.size;
        if (clearBtn) clearBtn.style.display = activePool.size > 0 ? 'inline-block' : 'none';
        if (lockAlert) lockAlert.style.display = activePool.size === 0 ? 'block' : 'none';

        if (activePool.size === 0) {{
            container.innerHTML = '<div class="empty-pool-notice">No rate-up units selected yet. Tap <strong>"+ Add to Pool"</strong> below to add units!</div>';
            return;
        }}
        const pills = [];
        activePool.forEach(id => {{
            const u = unitMap[id] || {{ id: id, name: 'Unit ' + id, rarity: 'NV' }};
            const badgeCls = u.rarity === 'NV+' ? 'badge-nvplus' : (u.rarity === 'NV' ? 'badge-nv' : 'badge-star5');
            pills.push(
                '<div class="pool-pill">' +
                    '<span class="badge ' + badgeCls + '">' + u.rarity + '</span>' +
                    '<span class="pill-name">' + u.name + '</span>' +
                    '<span class="pill-id">#' + u.id + '</span>' +
                    '<button type="button" class="pill-remove-btn" onclick="togglePoolUnit(\\'remove\\', \\'' + u.id + '\\')" title="Remove unit">✕</button>' +
                '</div>'
            );
        }});
        container.innerHTML = pills.join('');
    }}

    window.togglePoolUnit = function(action, id) {{
        const u = unitMap[id] || {{ id: id, name: 'Unit ' + id }};
        const url = '/exvius/gacha-rates/9900001.html?action=' + action + '&id=' + id + '&format=json';
        fetch(url)
            .then(res => res.json())
            .then(data => {{
                if (data && data.pool !== undefined) {{
                    activePool = new Set(data.pool);
                }} else if (action === 'add') {{
                    activePool.add(id);
                }} else {{
                    activePool.delete(id);
                }}
                renderActivePool();
                applyUnitFilter();
                const unlockMsg = (action === 'add' && activePool.size === 1) ? ' (Banner Unlocked!)' : '';
                showToast((action === 'add' ? 'Added ' : 'Removed ') + u.name + unlockMsg);
            }})
            .catch(() => {{
                // Fallback direct navigation
                window.location.href = '/exvius/gacha-rates/9900001.html?' + (action === 'add' ? 'add_unit=' : 'remove_unit=') + id;
            }});
    }};

    window.clearPool = function() {{
        if (!confirm('Clear all rate-up units from the pool?')) return;
        fetch('/exvius/gacha-rates/9900001.html?action=clear&format=json')
            .then(res => res.json())
            .then(data => {{
                activePool = new Set(data.pool || []);
                renderActivePool();
                applyUnitFilter();
                showToast('Rate-up pool cleared');
            }})
            .catch(() => {{
                window.location.href = '/exvius/gacha-rates/9900001.html?clear_pool=1';
            }});
    }};

    window.selectRarityFilter = function(rarity) {{
        activeRarity = rarity;
        document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
        if (rarity === 'all') document.getElementById('pillAll').classList.add('active');
        else if (rarity === 'NV+') document.getElementById('pillNVPlus').classList.add('active');
        else if (rarity === 'NV') document.getElementById('pillNV').classList.add('active');
        else document.getElementById('pill5').classList.add('active');
        applyUnitFilter();
    }};

    window.applyUnitFilter = function() {{
        const input = document.getElementById('unitSearchInput');
        const q = (input ? input.value : '').trim().toLowerCase();
        const list = document.getElementById('unitResultsList');
        if (!list) return;

        const filtered = allUnits.filter(u => {{
            const matchRarity = (activeRarity === 'all') || (u.rarity === activeRarity);
            const matchSearch = !q || u.name.toLowerCase().includes(q) || u.id.includes(q);
            return matchRarity && matchSearch;
        }});

        if (!filtered.length) {{
            list.innerHTML = '<div style="padding: 24px; text-align: center; color: #8bb1db;">No units matching "' + q + '" found.</div>';
            return;
        }}

        list.innerHTML = filtered.map(u => {{
            const inPool = activePool.has(u.id);
            const badgeCls = u.rarity === 'NV+' ? 'badge-nvplus' : (u.rarity === 'NV' ? 'badge-nv' : 'badge-star5');
            return '<div class="unit-item' + (inPool ? ' in-pool-row' : '') + '">' +
                '<div class="unit-left">' +
                    '<span class="badge ' + badgeCls + '">' + u.rarity + '</span>' +
                    '<span class="item-name">' + u.name + '</span>' +
                    '<span class="item-id">#' + u.id + '</span>' +
                '</div>' +
                '<div class="unit-right">' +
                    (inPool
                        ? '<button type="button" class="btn-in-pool" onclick="togglePoolUnit(\\'remove\\', \\'' + u.id + '\\')">✓ IN POOL (Remove)</button>'
                        : '<button type="button" class="btn-add-pool" onclick="togglePoolUnit(\\'add\\', \\'' + u.id + '\\')">+ Add to Pool</button>') +
                '</div>' +
            '</div>';
        }}).join('');
    }};

    renderActivePool();
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', applyUnitFilter);
    }} else {{
        applyUnitFilter();
    }}
}})();
</script>
'''


def page(banner_id):
    from ffbe_gacha import all_banners
    from player_state import expand_pool
    banner = next((b for b in all_banners() if str(b['id']) == str(banner_id)), None)
    if banner is None:
        return None
    notice = ('Choose a unit or prism from the selection list.' if banner.get('selection') else
              'The rates below apply to this summon. Guaranteed slots and additional rewards are listed separately.')
    body = '<h1>' + escape(banner['name']) + '</h1><p class="notice">' + escape(notice).replace('\n', '<br>') + '</p>'
    if str(banner_id) == '9900001':
        import ffbe_state as st
        cur_pool = []
        if st.State.player:
            cur_pool = list(st.State.player.data.get('custom_stepup_pool') or [])
            if not cur_pool and st.State.player.data.get('custom_stepup_unit'):
                cur_pool = [str(st.State.player.data['custom_stepup_unit'])]
        body = _custom_stepup_picker_html(cur_pool) + '<hr style="border: 0; border-top: 1px solid #234b79; margin: 24px 0;">' + body
    if banner.get('boxes'):
        body += '<p>The first five boxes draw without replacement. Remaining quantities and featured rewards appear in the original Box Details screen.</p>'
        body += '<h2>Standard pool after the five boxes</h2><p>Materials 80%, enhancers 19%, ultra-rare rewards 1%, divided equally within each group.</p>'
    if banner.get('selection'):
        from exvius_actions import _mst
        from ffbe_gacha import unit_name
        choices = _mst('F_GACHA_SELECT_UNIT_MST.ndjson', '3HriTp6B')
        body += '<table><thead><tr><th>Selectable unit</th><th>Select tickets</th></tr></thead><tbody>' + ''.join(
            '<tr><td>' + escape(unit_name(iid)) + '</td><td>' + row['e4mG8jTc'] + '</td></tr>'
            for iid, row in choices.items()) + '</tbody></table>'
    offers = banner.get('steps') or [banner]
    if not banner.get('steps') and banner.get('secondary_offer'):
        offers = [banner, banner['secondary_offer']]
    for index, offer in enumerate([] if banner.get('selection') else offers):
        if banner.get('steps'):
            body += '<h2>Step ' + str(index + 1) + '</h2>'
        elif len(offers) > 1:
            body += '<h2>' + ('Single summon' if index == 0 else 'Multi-summon') + '</h2>'
        cost = offer.get('cost', banner.get('cost', {}))
        if isinstance(cost, dict):
            amount = int(cost.get('amount', 0))
            currency = cost.get('kind', 'free')
            if cost.get('item_id'):
                currency = _item_names().get(str(cost['item_id']), 'Item ' + str(cost['item_id']))
            body += '<p>' + str(offer.get('draws', banner.get('draws', 1))) + ' draws. Cost: ' + (
                str(amount) + ' ' + escape(currency) if amount else 'Free') + '.</p>'
        definition = dict(banner)
        if 'pool' in offer:
            definition['pool'] = offer['pool']
        pool = banner.get('reward_pool') or expand_pool(definition)
        body += _table(pool, bool(banner.get('reward_pool')))
        guarantee = offer.get('guarantee', banner.get('guarantee', {}))
        if guarantee:
            count = int(guarantee.get('count', 1))
            if guarantee.get('rarity'):
                body += '<p>' + str(count) + ' guaranteed reward(s) of rarity ' + str(guarantee['rarity']) + ' or higher.</p>'
                restricted = expand_pool({'pool': guarantee['pool']}) if guarantee.get('pool') else pool
                restricted = [r for r in restricted if int(r.get('rarity', 0)) >= int(guarantee['rarity'])]
                body += '<h3>Guaranteed slot rates</h3>' + _table(restricted)
            if guarantee.get('unit_id'):
                from ffbe_gacha import unit_name
                body += '<p>Guaranteed unit: ' + escape(unit_name(guarantee['unit_id'])) + '.</p>'
        bonuses = offer.get('bonus_rewards', banner.get('bonus_rewards', []))
        for slot in offer.get('guarantee_slots', banner.get('guarantee_slots', [])):
            body += '<h3>' + str(slot.get('count', 1)) + ' guaranteed ' + escape(slot.get('label', 'reward')) + '</h3>'
            body += _table(expand_pool({'pool': slot['pool']}))
        if bonuses:
            body += '<h3>Additional rewards</h3><ul>' + ''.join(
                '<li>' + escape(reward_name(r)) + ' x' + str(r['count']) + '</li>' for r in bonuses) + '</ul>'
        choices = offer.get('bonus_choice', banner.get('bonus_choice', []))
        if choices:
            total = sum(float(choice['rate']) for choice in choices)
            body += '<h3>Bonus alternatives</h3><ul>' + ''.join('<li>' +
                ', '.join(escape(reward_name(r)) + ' x' + str(r['count']) for r in choice['rewards']) +
                ': %.2f%%</li>' % (float(choice['rate']) * 100 / total) for choice in choices) + '</ul>'
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Summon Rates</title><style>body{margin:0;padding:14px;background:#081d43;color:white;font:16px Arial}'
            'h1{font-size:21px}h1,h2,h3{color:#ffe398}.notice{padding:12px;background:#15385b;line-height:1.5}'
            'table{width:100%;border-collapse:collapse}th,td{padding:9px;border:1px solid #4b6990;text-align:left}'
            'td:last-child{white-space:nowrap}th{background:#194875}'
            '.custom-stepup-card{background:#0c203f;border:2px solid #2a588b;border-radius:8px;padding:16px;margin-bottom:20px;box-shadow:0 4px 12px rgba(0,0,0,0.4)}'
            '.stepup-header-badge{display:inline-block;background:#c2881b;color:#fff;font-size:11px;font-weight:bold;letter-spacing:1px;padding:3px 8px;border-radius:4px;margin-bottom:4px}'
            '.active-pool-container{background:#13325b;border-left:4px solid #ffd700;padding:12px 14px;border-radius:4px;margin-bottom:16px}'
            '.active-pool-pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}'
            '.pool-pill{display:inline-flex;align-items:center;gap:6px;background:#183e6d;border:1px solid #36659c;padding:4px 8px 4px 10px;border-radius:16px;font-size:13px;color:#fff}'
            '.pill-name{font-weight:bold}'
            '.pill-id{font-size:11px;color:#8bb1db}'
            '.pill-remove-btn{background:#e53935;color:white;border:none;border-radius:50%;width:18px;height:18px;font-size:10px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;padding:0;margin-left:4px}'
            '.clear-pool-btn{background:transparent;border:1px solid #e53935;color:#ff8a80;border-radius:4px;padding:2px 8px;font-size:11px;cursor:pointer}'
            '.clear-pool-btn:hover{background:#e53935;color:white}'
            '.empty-pool-notice{color:#8bb1db;font-size:13px;padding:4px 0}'
            '.badge{display:inline-block;padding:3px 8px;font-size:12px;font-weight:bold;border-radius:4px;text-shadow:0 1px 2px rgba(0,0,0,0.5)}'
            '.badge-nvplus,.badge.nvplus{background:linear-gradient(135deg,#7b1fa2,#00e5ff);color:white;box-shadow:0 0 6px rgba(0,229,255,0.6)}'
            '.badge-nv,.badge.nv{background:linear-gradient(135deg,#e91e63,#9c27b0);color:white}'
            '.badge-star5,.badge.star5{background:linear-gradient(135deg,#fbc02d,#f57c00);color:black}'
            '.filter-toolbar{display:flex;flex-direction:column;gap:8px;margin-bottom:12px}'
            '#unitSearchInput{width:100%;box-sizing:border-box;background:#08172c;border:1px solid #365b87;border-radius:6px;padding:10px 14px;font-size:15px;color:white;outline:none}'
            '#unitSearchInput:focus{border-color:#ffe398}'
            '.filter-pills{display:flex;gap:8px}'
            '.pill-btn{background:#163761;border:1px solid #2b5585;color:#b7d6fb;border-radius:20px;padding:6px 14px;font-size:13px;font-weight:bold;cursor:pointer}'
            '.pill-btn.active{background:#ffe398;color:#0a1b33;border-color:#ffd700}'
            '.unit-picker-scroll{max-height:380px;overflow-y:auto;background:#08172c;border:1px solid #254b77;border-radius:6px}'
            '.unit-results-list{display:flex;flex-direction:column}'
            '.unit-item{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-bottom:1px solid #142f52}'
            '.unit-item:last-child{border-bottom:none}'
            '.unit-item.in-pool-row{background:#11385f}'
            '.unit-left{display:flex;align-items:center;gap:10px;flex-wrap:wrap}'
            '.item-name{font-size:15px;font-weight:bold;color:white}'
            '.item-id{font-size:12px;color:#7899be}'
            '.btn-add-pool{background:#1976d2;color:white;border:none;padding:6px 14px;border-radius:4px;font-size:13px;font-weight:bold;cursor:pointer;white-space:nowrap}'
            '.btn-add-pool:hover{background:#2196f3}'
            '.btn-in-pool{background:#2e7d32;color:white;border:none;padding:6px 14px;border-radius:4px;font-size:13px;font-weight:bold;cursor:pointer;white-space:nowrap}'
            '.btn-in-pool:hover{background:#d32f2f}'
            '.toast-popup{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1b5e20;color:white;padding:10px 20px;border-radius:24px;font-size:14px;font-weight:bold;box-shadow:0 4px 12px rgba(0,0,0,0.5);opacity:0;transition:opacity 0.3s;pointer-events:none;z-index:9999}'
            '.toast-popup.show{opacity:1}'
            '</style></head><body>' + body + '</body></html>')
