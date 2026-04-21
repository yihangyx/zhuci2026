<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>自动注册增强版 | 临时邮箱 + 批量注册</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #EFF3F8;
            font-family: 'Inter', 'Segoe UI', '微软雅黑', system-ui, sans-serif;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        /* 头部 */
        .header {
            background: linear-gradient(135deg, #1E2A3A, #0F172A);
            border-radius: 28px;
            padding: 20px 28px;
            margin-bottom: 24px;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        .header h1 { font-size: 1.8rem; letter-spacing: -0.3px; }
        .badge { background: #FFB347; color: #1E2A3A; padding: 6px 14px; border-radius: 40px; font-weight: 600; font-size: 0.8rem; }

        /* 双栏布局 */
        .grid-2col {
            display: flex;
            gap: 24px;
            flex-wrap: wrap;
        }
        .card {
            background: white;
            border-radius: 28px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            padding: 24px;
            transition: all 0.2s;
        }
        .form-card { flex: 1.2; min-width: 320px; }
        .log-card { flex: 0.9; min-width: 280px; display: flex; flex-direction: column; }

        .field-row {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 8px;
        }
        .field-row label {
            width: 80px;
            font-weight: 500;
            color: #1E293B;
        }
        input, select {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #CBD5E1;
            border-radius: 20px;
            font-size: 0.9rem;
            background: #FEFEFE;
            transition: 0.2s;
            outline: none;
        }
        input:focus { border-color: #4F46E5; box-shadow: 0 0 0 3px rgba(79,70,229,0.1); }

        .btn-group {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin: 20px 0 16px;
        }
        .btn {
            padding: 10px 20px;
            border-radius: 40px;
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: 0.2s;
            background: #F1F5F9;
            color: #1E293B;
        }
        .btn-primary { background: #4F46E5; color: white; box-shadow: 0 2px 6px rgba(79,70,229,0.3); }
        .btn-primary:hover { background: #4338CA; transform: translateY(-1px);}
        .btn-success { background: #16A34A; color: white; }
        .btn-danger { background: #DC2626; color: white; }
        .btn-warning { background: #FF9800; color: white; }
        .btn-outline { background: white; border: 1px solid #CBD5E1; }

        .batch-panel {
            background: #F8FAFE;
            border-radius: 24px;
            padding: 16px;
            margin-top: 16px;
            border: 1px solid #E2E8F0;
        }

        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
            padding-top: 12px;
            border-top: 1px solid #EDF2F7;
            font-size: 0.85rem;
        }

        .log-box {
            background: #0F172A;
            color: #E2E8F0;
            border-radius: 20px;
            height: 460px;
            overflow-y: auto;
            font-family: 'JetBrains Mono', 'Consolas', monospace;
            font-size: 0.8rem;
            padding: 16px;
            margin-top: 12px;
        }
        .log-line {
            padding: 6px 0;
            border-bottom: 1px solid #2D3A4A;
            white-space: pre-wrap;
            word-break: break-all;
        }
        .log-success { color: #4ADE80; }
        .log-error { color: #F87171; }
        .log-warning { color: #FBBF24; }

        .record-table {
            width: 100%;
            font-size: 0.8rem;
            border-collapse: collapse;
            margin-top: 12px;
        }
        .record-table th, .record-table td {
            text-align: left;
            padding: 8px 4px;
            border-bottom: 1px solid #E2E8F0;
        }
        .btn-icon {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1.1rem;
        }
        @media (max-width: 700px) {
            .field-row { flex-direction: column; align-items: flex-start; }
            .field-row label { width: auto; }
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div>
            <h1>⚡ 自动注册工作台</h1>
            <div style="font-size:0.85rem; opacity:0.8;">临时邮箱 · 验证码自动识别 · 批量注册</div>
        </div>
        <div class="badge">by 奕涵 | 仅限临时用途</div>
    </div>

    <div class="grid-2col">
        <!-- 左侧表单区 -->
        <div class="card form-card">
            <div class="field-row">
                <label>用户名</label>
                <input type="text" id="username" placeholder="自动生成或手动填写">
            </div>
            <div class="field-row">
                <label>密码</label>
                <input type="text" id="password" placeholder="随机生成">
            </div>
            <div class="field-row">
                <label>邮箱</label>
                <input type="text" id="email" placeholder="点击「生成邮箱」">
            </div>
            <div class="field-row">
                <label>邀请人</label>
                <input type="text" id="invite" placeholder="选填">
            </div>
            <div class="field-row">
                <label>验证码</label>
                <input type="text" id="code" placeholder="自动填写或手动">
            </div>

            <div class="btn-group">
                <button id="randomBtn" class="btn btn-primary">🎲 随机账号</button>
                <button id="genEmailBtn" class="btn btn-primary" style="background:#0099FF;">📬 生成邮箱</button>
                <button id="sendCodeBtn" class="btn btn-warning">📨 发送验证码</button>
                <button id="refreshMailBtn" class="btn btn-outline">🔄 刷新邮件</button>
                <button id="registerBtn" class="btn btn-success">✅ 立即注册</button>
            </div>



            <div class="status-bar">
                <span id="statusMsg" style="color:#16A34A; font-weight:500;">● 就绪</span>
                <span id="successCountBadge" style="background:#EFF6FF; padding:4px 12px; border-radius:40px;">✅ 成功: 0</span>
            </div>
        </div>

        <!-- 右侧日志 + 记录 -->
        <div class="card log-card">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-weight: 700;">📋 实时日志</span>
                <button id="clearLogBtn" class="btn-icon" title="清空日志">🗑️</button>
            </div>
            <div id="logPanel" class="log-box">
                <div class="log-line">✨ 工具启动完成 | 支持批量注册</div>
                <div class="log-line">📌 流程: 生成邮箱 → 发验证码 → 刷新邮件(自动填码) → 注册</div>
                <div class="log-line">━━━━━━━━━━━━━━━━━━━━━━━━━━</div>
            </div>
            <div style="margin-top: 16px;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: 700;">📝 注册成功记录</span>
                    <button id="exportCsvBtn" class="btn-icon" title="导出CSV">⬇️ 导出</button>
                </div>
                <div style="max-height: 180px; overflow-y: auto;">
                    <table class="record-table" id="recordTable">
                        <thead><tr><th>账号</th><th>密码</th><th>邮箱</th><th>时间</th></tr></thead>
                        <tbody id="recordBody"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    // ======================== 工具函数 ========================
    function randomString(len=8) {
        const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
        return Array.from({length:len},()=>chars[Math.floor(Math.random()*chars.length)]).join('');
    }
    function randomUsername() {
        const prefixes = ['user','test','demo','auto','reg'];
        return prefixes[Math.floor(Math.random()*prefixes.length)] + Math.floor(Math.random()*9000+1000);
    }
    function randomPassword() {
        const lower = "abcdefghijklmnopqrstuvwxyz";
        const upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        const digits = "0123456789";
        let p = '';
        for(let i=0;i<4;i++) p+=lower[Math.floor(Math.random()*lower.length)];
        for(let i=0;i<2;i++) p+=upper[Math.floor(Math.random()*upper.length)];
        for(let i=0;i<3;i++) p+=digits[Math.floor(Math.random()*digits.length)];
        return p.split('').sort(()=>Math.random()-0.5).join('');
    }

    // 日志
    const logPanel = document.getElementById('logPanel');
    function addLog(msg, type='info') {
        const div = document.createElement('div');
        div.className = `log-line log-${type}`;
        div.innerText = msg;
        logPanel.appendChild(div);
        div.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        while(logPanel.children.length > 300) logPanel.removeChild(logPanel.firstChild);
    }

    // UI元素
    const usernameInp = document.getElementById('username');
    const passwordInp = document.getElementById('password');
    const emailInp = document.getElementById('email');
    const inviteInp = document.getElementById('invite');
    const codeInp = document.getElementById('code');
    const statusSpan = document.getElementById('statusMsg');
    const successBadge = document.getElementById('successCountBadge');
    let successCount = 0;
    function updateSuccessUI() { successBadge.innerText = `✅ 成功: ${successCount}`; }

    function setStatus(text, isError=false) {
        statusSpan.innerText = text;
        statusSpan.style.color = isError ? '#DC2626' : '#16A34A';
    }

    // 成功记录存储
    let records = [];
    function addRecord(username, password, email) {
        records.unshift({ username, password, email, time: new Date().toLocaleTimeString() });
        if(records.length > 50) records.pop();
        renderRecords();
    }
    function renderRecords() {
        const tbody = document.getElementById('recordBody');
        tbody.innerHTML = '';
        records.forEach(r => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${escapeHtml(r.username)}</td><td>${escapeHtml(r.password)}</td><td>${escapeHtml(r.email)}</td><td>${r.time}</td>`;
            tbody.appendChild(tr);
        });
    }
    function exportCSV() {
        if(records.length===0) { addLog("暂无记录可导出",'warning'); return; }
        let csv = "账号,密码,邮箱,时间\n";
        records.forEach(r=>{ csv += `"${r.username}","${r.password}","${r.email}","${r.time}"\n`; });
        const blob = new Blob(["\uFEFF" + csv], {type: "text/csv;charset=utf-8;"});
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.href = url;
        link.setAttribute("download","注册账号记录.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        addLog("📎 导出成功",'success');
    }
    function escapeHtml(str) { return str.replace(/[&<>]/g, function(m){if(m==='&') return '&amp;'; if(m==='<') return '&lt;'; if(m==='>') return '&gt;'; return m;}); }

    // ======================== Mail.tm API 封装 ========================
    class MailTMApi {
        constructor() { this.baseUrl='https://api.mail.tm'; this.token=null; this.address=null; this.password=null; }
        async reset() { this.token=null; this.address=null; this.password=null; }
        async getDomains() { try{ const r=await fetch(`${this.baseUrl}/domains`); const d=await r.json(); return d['hydra:member']||[]; }catch(e){return [];} }
        async createAccount(username=null) {
            const domains=await this.getDomains();
            if(!domains.length) return null;
            const domain=domains[0].domain;
            const finalUser=username || `u${randomString(8)}`;
            const pwd=randomPassword();
            const address=`${finalUser}@${domain}`;
            try{
                const resp=await fetch(`${this.baseUrl}/accounts`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({address,password:pwd})});
                if(resp.status===201){
                    this.address=address; this.password=pwd;
                    return address;
                } return null;
            }catch(e){return null;}
        }
        async getToken(){
            if(!this.address||!this.password) return null;
            try{
                const resp=await fetch(`${this.baseUrl}/token`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({address:this.address,password:this.password})});
                if(resp.ok){ const data=await resp.json(); this.token=data.token; return this.token; }
                return null;
            }catch(e){return null;}
        }
        async getMessages(){
            if(!this.token) await this.getToken();
            if(!this.token) return [];
            try{
                const resp=await fetch(`${this.baseUrl}/messages`,{headers:{'Authorization':`Bearer ${this.token}`}});
                const data=await resp.json();
                return data['hydra:member']||[];
            }catch(e){return [];}
        }
        async getMessageContent(msgId){
            if(!this.token) await this.getToken();
            if(!this.token) return null;
            try{
                const resp=await fetch(`${this.baseUrl}/messages/${msgId}`,{headers:{'Authorization':`Bearer ${this.token}`}});
                return await resp.json();
            }catch(e){return null;}
        }
        async extractSixDigitCode(){
            const msgs=await this.getMessages();
            for(const msg of msgs){
                const full=await this.getMessageContent(msg.id);
                if(!full) continue;
                const text=(full.text||'')+(full.html||'');
                const match=text.match(/\b\d{6}\b/g);
                if(match && match.length) return match[0];
            }
            return null;
        }
        async fetchAndShowMessages(){
            if(!this.address) throw new Error('无邮箱');
            const msgs=await this.getMessages();
            if(!msgs.length){ addLog('📭 暂无新邮件','warning'); return null; }
            for(const msg of msgs){
                const subject=msg.subject||'无标题';
                const fromAddr=msg.from?.address||'未知';
                const full=await this.getMessageContent(msg.id);
                const content=(full?.text||full?.html||'').substring(0,300);
                addLog(`📩 标题: ${subject} | 发件人: ${fromAddr}`, 'info');
                if(content) addLog(`   内容预览: ${content.replace(/\n/g,' ')}`,'info');
            }
            const code=await this.extractSixDigitCode();
            return code;
        }
    }

    class JSAutoTaskClient {
        constructor(){ this.baseUrl='https://jsautotask.com'; }
        
        // 修复发送验证码: 添加必要的 headers 和 withCredentials
        async sendEmailCode(email){
            try{
                const response = await fetch(`${this.baseUrl}/api/register/getEmail`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json, text/plain, */*'
                    },
                    body: JSON.stringify({ email }),
                    credentials: 'include',   // 携带cookie
                    mode: 'cors'              // 明确cors模式
                });
                
                if(!response.ok){
                    const errorText = await response.text();
                    throw new Error(`HTTP ${response.status}: ${errorText}`);
                }
                
                const data = await response.json();
                return data;
            } catch(err){
                console.error("sendEmailCode error:", err);
                return { error: err.message || '网络请求失败', succeed: false };
            }
        }
        
        async register(username, password, email, emailCode, inviteUser=''){
            try{
                const resp=await fetch(`${this.baseUrl}/api/register/register`,{
                    method:'POST',
                    headers:{'Content-Type':'application/json','Accept':'application/json, text/plain, */*'},
                    body:JSON.stringify({username,password,confirmPassword:password,email,emailCode,inviteUser}),
                    credentials:'include',
                    mode:'cors'
                });
                if(!resp.ok){
                    const txt = await resp.text();
                    throw new Error(`HTTP ${resp.status}`);
                }
                return await resp.json();
            } catch(e){ 
                console.error("register error", e);
                return { error:e.message, succeed:false }; 
            }
        }
    }

    // ======================== 全局状态 ========================
    let mailApi = new MailTMApi();
    let regClient = new JSAutoTaskClient();

    // 核心注册流程 (返回是否成功)
    async function runSingleRegister() {
        // 1. 生成随机账号密码（如果当前输入框为空则生成填充）
        let username = usernameInp.value.trim();
        let password = passwordInp.value.trim();
        if(!username) { username = randomUsername(); usernameInp.value = username; }
        if(!password) { password = randomPassword(); passwordInp.value = password; }
        const invite = inviteInp.value.trim();

        // 2. 生成新邮箱 (重置邮箱状态)
        await mailApi.reset();
        const email = await mailApi.createAccount();
        if(!email) { addLog("❌ 生成邮箱失败",'error'); return false; }
        emailInp.value = email;
        codeInp.value = '';
        addLog(`📧 新邮箱: ${email}`, 'success');

        // 3. 发送验证码 (增加重试机制)
        let sendSuccess = false;
        let sendErrMsg = '';
        for(let attempt=1; attempt<=2; attempt++){
            addLog(`📨 发送验证码到 ${email} ... (尝试 ${attempt}/2)`, 'info');
            const sendRes = await regClient.sendEmailCode(email);
            if(sendRes && (sendRes.succeed === true || sendRes.code === 200 || sendRes.status === 'success')) {
                sendSuccess = true;
                addLog(`✅ 验证码已发送，等待几秒后提取...`, 'success');
                break;
            } else {
                sendErrMsg = sendRes?.message || sendRes?.data || sendRes?.error || '未知错误';
                addLog(`⚠️ 发送尝试 ${attempt} 失败: ${sendErrMsg}`, 'warning');
                if(attempt === 1) await new Promise(r => setTimeout(r, 2000));
            }
        }
        if(!sendSuccess){
            addLog(`❌ 发送验证码最终失败: ${sendErrMsg}`, 'error');
            return false;
        }

        // 4. 轮询获取验证码 (最多等待25秒，每3秒尝试)
        let retries = 0;
        let verifyCode = null;
        while(retries < 8 && !verifyCode) {
            await new Promise(r => setTimeout(r, 3000));
            addLog(`🔍 第${retries+1}次尝试获取验证码...`,'info');
            try {
                const code = await mailApi.fetchAndShowMessages();
                if(code && /^\d{6}$/.test(code)) {
                    verifyCode = code;
                    break;
                }
            } catch(e) {
                addLog(`获取邮件异常: ${e.message}`, 'warning');
            }
            retries++;
        }
        if(!verifyCode) {
            addLog(`❌ 未获取到6位验证码，注册失败`, 'error');
            return false;
        }
        codeInp.value = verifyCode;
        addLog(`🎯 识别验证码: ${verifyCode}`, 'success');

        // 5. 执行注册
        const regRes = await regClient.register(username, password, email, verifyCode, invite);
        if(regRes && regRes.succeed === true) {
            successCount++;
            updateSuccessUI();
            addRecord(username, password, email);
            addLog(`🎉 注册成功! 账号:${username} 密码:${password}`, 'success');
            setStatus(`成功: ${username}`, false);
            return true;
        } else {
            const err = regRes?.data || regRes?.message || regRes?.error || '未知错误';
            addLog(`❌ 注册失败: ${err}`, 'error');
            return false;
        }
    }

    // 单次注册（使用当前UI输入或自动生成）
    async function singleRegister() {
        setStatus("注册中...", false);
        await runSingleRegister();
        setStatus("就绪", false);
    }

    // 独立函数绑定
    async function generateEmail() {
        await mailApi.reset();
        const email = await mailApi.createAccount();
        if(email) {
            emailInp.value = email;
            codeInp.value = '';
            addLog(`📧 新邮箱: ${email}`, 'success');
            setStatus("邮箱已生成", false);
        } else { addLog("邮箱生成失败",'error'); }
    }
    async function sendCode() {
        const email = emailInp.value.trim();
        if(!email) { addLog("请先生成邮箱",'warning'); return; }
        const res = await regClient.sendEmailCode(email);
        if(res.succeed === true || res.code === 200) {
            addLog("✅ 验证码已发送，稍后点击刷新邮件获取",'success');
        } else {
            addLog(`❌ 发送失败: ${res.message || res.data || res.error || '未知错误'}`, 'error');
        }
    }
    async function refreshAndFill() {
        if(!mailApi.address) { addLog("没有邮箱，请先生成",'warning'); return; }
        addLog("刷新邮件并识别验证码...",'info');
        const code = await mailApi.fetchAndShowMessages();
        if(code) { codeInp.value = code; addLog(`✅ 验证码填入: ${code}`,'success'); }
        else addLog("未找到6位验证码",'error');
    }
    function randomAccount() {
        usernameInp.value = randomUsername();
        passwordInp.value = randomPassword();
        addLog("随机账号密码已填入",'success');
    }

    // 事件绑定
    document.getElementById('randomBtn').onclick = randomAccount;
    document.getElementById('genEmailBtn').onclick = generateEmail;
    document.getElementById('sendCodeBtn').onclick = sendCode;
    document.getElementById('refreshMailBtn').onclick = refreshAndFill;
    document.getElementById('registerBtn').onclick = singleRegister;
    document.getElementById('clearLogBtn').onclick = () => { logPanel.innerHTML = '<div class="log-line">✨ 日志已清空</div>'; };
    document.getElementById('exportCsvBtn').onclick = exportCSV;

    updateSuccessUI();
    addLog("🔧 已修复发送验证码的请求头与跨域问题", 'success');
</script>
</body>
</html>