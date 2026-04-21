const express = require('express');
const fetch = require('node-fetch');
const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(express.json());
app.use(express.static('public'));

// 工具函数
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

// Mail.tm API 封装
class MailTMApi {
    constructor() {
        this.baseUrl = 'https://api.mail.tm';
        this.token = null;
        this.address = null;
        this.password = null;
    }
    
    async reset() {
        this.token = null;
        this.address = null;
        this.password = null;
    }
    
    async getDomains() {
        try {
            const r = await fetch(`${this.baseUrl}/domains`);
            const d = await r.json();
            return d['hydra:member'] || [];
        } catch(e) {
            return [];
        }
    }
    
    async createAccount(username = null) {
        const domains = await this.getDomains();
        if(!domains.length) return null;
        const domain = domains[0].domain;
        const finalUser = username || `u${randomString(8)}`;
        const pwd = randomPassword();
        const address = `${finalUser}@${domain}`;
        
        try {
            const resp = await fetch(`${this.baseUrl}/accounts`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ address, password: pwd })
            });
            
            if(resp.status === 201) {
                this.address = address;
                this.password = pwd;
                return address;
            }
            return null;
        } catch(e) {
            return null;
        }
    }
    
    async getToken() {
        if(!this.address || !this.password) return null;
        
        try {
            const resp = await fetch(`${this.baseUrl}/token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ address: this.address, password: this.password })
            });
            
            if(resp.ok) {
                const data = await resp.json();
                this.token = data.token;
                return this.token;
            }
            return null;
        } catch(e) {
            return null;
        }
    }
    
    async getMessages() {
        if(!this.token) await this.getToken();
        if(!this.token) return [];
        
        try {
            const resp = await fetch(`${this.baseUrl}/messages`, {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await resp.json();
            return data['hydra:member'] || [];
        } catch(e) {
            return [];
        }
    }
    
    async getMessageContent(msgId) {
        if(!this.token) await this.getToken();
        if(!this.token) return null;
        
        try {
            const resp = await fetch(`${this.baseUrl}/messages/${msgId}`, {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            return await resp.json();
        } catch(e) {
            return null;
        }
    }
    
    async extractSixDigitCode() {
        const msgs = await this.getMessages();
        for(const msg of msgs) {
            const full = await this.getMessageContent(msg.id);
            if(!full) continue;
            const text = (full.text || '') + (full.html || '');
            const match = text.match(/\b\d{6}\b/g);
            if(match && match.length) return match[0];
        }
        return null;
    }
    
    async fetchAndShowMessages() {
        if(!this.address) throw new Error('无邮箱');
        const msgs = await this.getMessages();
        if(!msgs.length) return null;
        
        const code = await this.extractSixDigitCode();
        return code;
    }
}

// JSAutoTask 注册接口
class JSAutoTaskClient {
    constructor() {
        this.baseUrl = 'https://jsautotask.com';
    }
    
    async sendEmailCode(email) {
        try {
            const response = await fetch(`${this.baseUrl}/api/register/getEmail`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json, text/plain, */*',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
                },
                body: JSON.stringify({ email }),
                credentials: 'include'
            });
            
            if(!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
            
            const data = await response.json();
            return data;
        } catch(err) {
            console.error("sendEmailCode error:", err);
            return { error: err.message || '网络请求失败', succeed: false };
        }
    }
    
    async register(username, password, email, emailCode, inviteUser = '') {
        try {
            const resp = await fetch(`${this.baseUrl}/api/register/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json, text/plain, */*',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
                },
                body: JSON.stringify({ username, password, confirmPassword: password, email, emailCode, inviteUser }),
                credentials: 'include'
            });
            
            if(!resp.ok) {
                const txt = await resp.text();
                throw new Error(`HTTP ${resp.status}`);
            }
            return await resp.json();
        } catch(e) {
            console.error("register error", e);
            return { error: e.message, succeed: false };
        }
    }
}

// API 路由
app.post('/api/register', async (req, res) => {
    const { username, password, invite } = req.body;
    
    const mailApi = new MailTMApi();
    const regClient = new JSAutoTaskClient();
    
    try {
        // 1. 生成随机账号密码（如果未提供）
        const finalUsername = username || randomUsername();
        const finalPassword = password || randomPassword();
        const finalInvite = invite || '';
        
        // 2. 生成新邮箱
        await mailApi.reset();
        const email = await mailApi.createAccount();
        if(!email) {
            return res.json({ success: false, message: '生成邮箱失败' });
        }
        
        // 3. 发送验证码
        let sendSuccess = false;
        let sendErrMsg = '';
        
        for(let attempt=1; attempt<=2; attempt++) {
            const sendRes = await regClient.sendEmailCode(email);
            if(sendRes && (sendRes.succeed === true || sendRes.code === 200 || sendRes.status === 'success')) {
                sendSuccess = true;
                break;
            } else {
                sendErrMsg = sendRes?.message || sendRes?.data || sendRes?.error || '未知错误';
                if(attempt === 1) await new Promise(r => setTimeout(r, 2000));
            }
        }
        
        if(!sendSuccess) {
            return res.json({ success: false, message: `发送验证码失败: ${sendErrMsg}` });
        }
        
        // 4. 轮询获取验证码
        let retries = 0;
        let verifyCode = null;
        
        while(retries < 8 && !verifyCode) {
            await new Promise(r => setTimeout(r, 3000));
            try {
                const code = await mailApi.fetchAndShowMessages();
                if(code && /^\d{6}$/.test(code)) {
                    verifyCode = code;
                    break;
                }
            } catch(e) {
                console.error('获取邮件异常:', e);
            }
            retries++;
        }
        
        if(!verifyCode) {
            return res.json({ success: false, message: '未获取到6位验证码' });
        }
        
        // 5. 执行注册
        const regRes = await regClient.register(finalUsername, finalPassword, email, verifyCode, finalInvite);
        
        if(regRes && regRes.succeed === true) {
            return res.json({
                success: true,
                data: {
                    username: finalUsername,
                    password: finalPassword,
                    email: email
                }
            });
        } else {
            const err = regRes?.data || regRes?.message || regRes?.error || '未知错误';
            return res.json({ success: false, message: `注册失败: ${err}` });
        }
    } catch(err) {
        console.error('注册过程错误:', err);
        return res.json({ success: false, message: `服务器错误: ${err.message}` });
    }
});

// 静态文件服务
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

// 启动服务器
app.listen(PORT, () => {
    console.log(`服务器运行在 http://localhost:${PORT}`);
});
