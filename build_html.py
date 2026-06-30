#!/usr/bin/env python3
"""Generate the dual-subject quiz HTML."""

import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# Load merged questions
with open(os.path.join(script_dir, 'questions.json')) as f:
    questions = json.load(f)

json_str = json.dumps(questions, ensure_ascii=False)

# Count by subject and type
xi_singles = sum(1 for q in questions if q['subject'] == 'xi' and q['type'] == 'single')
xi_multis = sum(1 for q in questions if q['subject'] == 'xi' and q['type'] == 'multiple')
mao_singles = sum(1 for q in questions if q['subject'] == 'mao' and q['type'] == 'single')
mao_multis = sum(1 for q in questions if q['subject'] == 'mao' and q['type'] == 'multiple')
mao_judges = sum(1 for q in questions if q['subject'] == 'mao' and q['type'] == 'judge')
total_xi = xi_singles + xi_multis
total_mao = mao_singles + mao_multis + mao_judges

print(f"Xi: {total_xi} (single:{xi_singles}, multi:{xi_multis})")
print(f"Mao: {total_mao} (single:{mao_singles}, multi:{mao_multis}, judge:{mao_judges})")

# Build the HTML
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>思政复习题库</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--c-bg:#f5f0eb;--c-card:#fff;--c-primary:#8b1a1a;--c-primary-light:#a52a2a;--c-accent:#c41230;--c-text:#2c2c2c;--c-text-light:#666;--c-border:#e0d5c7;--c-correct:#2d7d46;--c-correct-bg:#e8f5e9;--c-wrong:#c62828;--c-wrong-bg:#ffebee;--c-mao:#1a5c8b;--c-mao-light:#2b7abf;--c-tag:#f0e6d8;--shadow:0 2px 8px rgba(0,0,0,0.06);--radius:10px}}
body{{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans SC","Microsoft YaHei",sans-serif;background:var(--c-bg);color:var(--c-text);line-height:1.7;min-height:100vh}}
.container{{max-width:800px;margin:0 auto;padding:16px}}
.header{{background:var(--c-primary);color:#fff;padding:16px 20px;text-align:center;position:sticky;top:0;z-index:100;box-shadow:0 2px 12px rgba(0,0,0,0.15)}}
.header h1{{font-size:1.25rem;font-weight:600;letter-spacing:.5px}}
.header .sub{{font-size:.8rem;opacity:.85;margin-top:2px}}
.nav{{display:flex;gap:8px;padding:12px 16px;background:var(--c-card);border-bottom:1px solid var(--c-border);overflow-x:auto;position:sticky;top:60px;z-index:99}}
.nav a{{white-space:nowrap;padding:6px 14px;border-radius:20px;text-decoration:none;font-size:.85rem;color:var(--c-text-light);background:var(--c-tag);transition:all .2s}}
.nav a.active,.nav a:hover{{background:var(--c-primary);color:#fff}}
.card{{background:var(--c-card);border-radius:var(--radius);box-shadow:var(--shadow);padding:20px;margin-bottom:16px}}
.card h2{{font-size:1.1rem;margin-bottom:12px;color:var(--c-primary)}}
.card.mao-card h2{{color:var(--c-mao)}}
.btn{{display:inline-block;padding:10px 22px;border:none;border-radius:8px;font-size:.95rem;cursor:pointer;text-decoration:none;text-align:center;transition:all .2s;font-weight:500}}
.btn-primary{{background:var(--c-primary);color:#fff}}
.btn-primary:hover{{background:var(--c-primary-light)}}
.btn-mao{{background:var(--c-mao);color:#fff}}
.btn-mao:hover{{background:var(--c-mao-light)}}
.btn-outline{{background:#fff;color:var(--c-primary);border:1.5px solid var(--c-primary)}}
.btn-outline:hover{{background:#fdf2f2}}
.btn-danger{{background:#fff;color:var(--c-wrong);border:1.5px solid var(--c-wrong)}}
.btn-danger:hover{{background:var(--c-wrong-bg)}}
.btn-sm{{padding:5px 12px;font-size:.8rem}}
.btn-block{{display:block;width:100%}}
.btn-group{{display:flex;gap:10px;flex-wrap:wrap}}
.stat-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px}}
.stat-item{{background:var(--c-tag);border-radius:var(--radius);padding:14px;text-align:center}}
.stat-item .num{{font-size:1.8rem;font-weight:700;color:var(--c-primary)}}
.stat-item.mao-stat .num{{color:var(--c-mao)}}
.stat-item .label{{font-size:.8rem;color:var(--c-text-light);margin-top:2px}}
.quiz-progress{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;font-size:.85rem;color:var(--c-text-light)}}
.progress-bar{{height:4px;background:var(--c-border);border-radius:2px;margin-bottom:20px;overflow:hidden}}
.progress-bar .fill{{height:100%;border-radius:2px;transition:width .3s}}
.progress-bar.xi .fill{{background:var(--c-primary)}}
.progress-bar.mao .fill{{background:var(--c-mao)}}
.question-block{{margin-bottom:20px}}
.question-text{{font-size:1rem;line-height:1.8}}
.options{{margin:16px 0}}
.option{{display:block;width:100%;text-align:left;padding:12px 16px;margin-bottom:8px;border:1.5px solid var(--c-border);border-radius:8px;background:#fff;cursor:pointer;transition:all .15s;font-size:.95rem;line-height:1.6}}
.option:hover{{border-color:var(--c-primary);background:#fdf8f6}}
.option.selected{{border-color:var(--c-primary);background:#fdf2f2}}
.option.correct{{border-color:var(--c-correct);background:var(--c-correct-bg);color:var(--c-correct)}}
.option.wrong{{border-color:var(--c-wrong);background:var(--c-wrong-bg);color:var(--c-wrong)}}
.option.disabled{{pointer-events:none;opacity:.85}}
.option-label{{display:inline-block;width:28px;height:28px;line-height:28px;text-align:center;border-radius:50%;background:var(--c-tag);margin-right:10px;font-weight:600;font-size:.85rem}}
.option.correct .option-label{{background:var(--c-correct);color:#fff}}
.option.wrong .option-label{{background:var(--c-wrong);color:#fff}}
.option.selected .option-label{{background:var(--c-primary);color:#fff}}
.option input[type="checkbox"]{{display:none}}
.option .check-mark{{display:inline-block;width:28px;height:28px;line-height:28px;text-align:center;border-radius:4px;background:var(--c-tag);margin-right:10px;font-weight:600;font-size:.85rem;vertical-align:middle}}
.option.selected .check-mark{{background:var(--c-primary);color:#fff}}
.option.correct .check-mark{{background:var(--c-correct);color:#fff}}
.option.wrong .check-mark{{background:var(--c-wrong);color:#fff}}
.feedback{{padding:12px 16px;border-radius:8px;margin:12px 0;font-size:.9rem;display:none}}
.feedback.show{{display:block}}
.feedback.correct-fb{{background:var(--c-correct-bg);color:var(--c-correct)}}
.feedback.wrong-fb{{background:var(--c-wrong-bg);color:var(--c-wrong)}}
.quiz-nav{{display:flex;gap:10px;justify-content:center;margin-top:20px}}
.table-wrap{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:.85rem}}
th,td{{padding:8px 10px;text-align:center;border-bottom:1px solid var(--c-border)}}
th{{background:var(--c-tag);font-weight:600;white-space:nowrap;position:sticky;top:0}}
td{{white-space:nowrap}}
tr:hover td{{background:#fdf8f6}}
.acc-high{{color:var(--c-correct);font-weight:600}}
.acc-mid{{color:#e67e22;font-weight:600}}
.acc-low{{color:var(--c-wrong);font-weight:600}}
.text-left{{text-align:left;white-space:normal;max-width:300px}}
.empty{{text-align:center;padding:40px 20px;color:var(--c-text-light)}}
.empty .icon{{font-size:3rem;margin-bottom:12px}}
@media(max-width:600px){{.container{{padding:10px}}.card{{padding:14px}}.header h1{{font-size:1.1rem}}.stat-grid{{grid-template-columns:repeat(2,1fr)}}.btn{{padding:8px 16px;font-size:.9rem}}}}
.tag{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.75rem;font-weight:600}}
.tag-single{{background:#e3f2fd;color:#1565c0}}
.tag-multiple{{background:#fff3e0;color:#e65100}}
.tag-judge{{background:#e8f5e9;color:#2e7d32}}
.tag-xi{{background:#fce4ec;color:#c62828}}
.tag-mao{{background:#e3f2fd;color:var(--c-mao)}}
.subject-tabs{{display:flex;gap:0;margin-bottom:16px;border-radius:8px;overflow:hidden}}
.subject-tab{{flex:1;padding:12px;text-align:center;cursor:pointer;border:none;font-size:.95rem;font-weight:500;transition:all .2s;background:var(--c-tag);color:var(--c-text-light)}}
.subject-tab.active{{background:var(--c-primary);color:#fff}}
.subject-tab.mao-tab.active{{background:var(--c-mao);color:#fff}}
.filter-bar{{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}}
.hint-text{{font-size:.7rem;color:var(--c-text-light);text-align:center;margin-bottom:10px}}
</style>
</head>
<body>

<div class="header">
  <h1>思政 · 复习题库</h1>
  <div class="sub">毛泽东思想 + 习近平思想 在线刷题</div>
</div>

<nav class="nav" id="mainNav">
  <a href="#home">🏠 首页</a>
  <a href="#quiz">📝 完整题库</a>
  <a href="#wrong">🎯 错题集</a>
  <a href="#stats">📊 作答统计</a>
  <a href="#history">📋 作答记录</a>
</nav>

<div class="container" id="app"><div class="loading">加载题库数据…</div></div>

<script>
const QUESTIONS = {json_str};

const STATS_KEY = 'xjp-xi-quiz-stats-v1';
const HISTORY_KEY = 'xjp-xi-quiz-attempts-v1';
const BACKUP_FILENAME = '思政题库备份.json';

let currentSubject = 'mao'; // default
let quizQuestions = [];
let quizIndex = 0;
let quizAnswered = {{}};

// ========== HELPERS ==========
function loadStats(){{try{{const r=localStorage.getItem(STATS_KEY);return r?JSON.parse(r):{{}}}}catch(e){{return{{}}}}}}
function saveStats(s){{localStorage.setItem(STATS_KEY,JSON.stringify(s))}}
function loadHistory(){{try{{const r=localStorage.getItem(HISTORY_KEY);return r?JSON.parse(r):[]}}catch(e){{return[]}}}}
function saveHistory(h){{localStorage.setItem(HISTORY_KEY,JSON.stringify(h))}}
function getQ(id){{return QUESTIONS.find(q=>q.id===id)}}
function shuffle(a){{const b=[...a];for(let i=b.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]]}}return b}}
function qsBySubject(subj){{return QUESTIONS.filter(q=>q.subject===subj)}}
function typeLabel(t){{return t==='single'?'单选题':t==='multiple'?'多选题':'判断题'}}
function typeTagClass(t){{return t==='single'?'tag-single':t==='multiple'?'tag-multiple':'tag-judge'}}

// ========== ROUTER ==========
function getPage(){{return window.location.hash.replace('#','')||'home'}}
function render(){{
  const page=getPage();
  document.querySelectorAll('#mainNav a').forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+page));
  const app=document.getElementById('app');
  switch(page){{
    case'home':renderHome(app);break;
    case'quiz':renderQuiz(app);break;
    case'wrong':renderWrong(app);break;
    case'stats':renderStats(app);break;
    case'history':renderHistory(app);break;
    default:renderHome(app);
  }}
}}
window.addEventListener('hashchange',render);

// ========== HOME PAGE ==========
function buildSubjectStats(subj){{
  const stats=loadStats();
  const qs=qsBySubject(subj);
  let attempted=0,totalCorrect=0,totalAttempts=0,wrongIds=[];
  for(const q of qs){{
    const s=stats[q.id];
    if(s&&s.attempts>0){{
      attempted++;totalCorrect+=s.correct;totalAttempts+=s.attempts;
      if(s.wrongRate>30)wrongIds.push(q.id);
    }}
  }}
  const accuracy=totalAttempts>0?Math.round(totalCorrect/totalAttempts*100):0;
  return{{total:qs.length,attempted,totalCorrect,totalAttempts,accuracy,wrongCount:wrongIds.length}};
}}

function renderHome(app){{
  const xi=buildSubjectStats('xi'),mao=buildSubjectStats('mao');
  app.innerHTML=`
    <div class="card">
      <h2>📖 学习状态</h2>
      <div class="stat-grid">
        <div class="stat-item"><div class="num">${{mao.total}}</div><div class="label">毛概题库</div></div>
        <div class="stat-item mao-stat"><div class="num">${{mao.attempted}}</div><div class="label">毛概已作答</div></div>
        <div class="stat-item mao-stat"><div class="num">${{mao.accuracy}}%</div><div class="label">毛概正确率</div></div>
        <div class="stat-item mao-stat"><div class="num">${{mao.wrongCount}}</div><div class="label">毛概错题</div></div>
      </div>
      <div class="stat-grid" style="margin-top:12px;">
        <div class="stat-item"><div class="num">${{xi.total}}</div><div class="label">习概题库</div></div>
        <div class="stat-item"><div class="num">${{xi.attempted}}</div><div class="label">习概已作答</div></div>
        <div class="stat-item"><div class="num">${{xi.accuracy}}%</div><div class="label">习概正确率</div></div>
        <div class="stat-item"><div class="num">${{xi.wrongCount}}</div><div class="label">习概错题</div></div>
      </div>
    </div>
    <div class="card">
      <h2>🚀 开始刷题</h2>
      <div class="btn-group" style="flex-direction:column;">
        <a class="btn btn-mao btn-block" href="#quiz" onclick="setSubject('mao')">📕 作答毛概题库（${{mao.total}} 题）</a>
        <a class="btn btn-mao btn-block" href="#wrong" onclick="setSubject('mao')">🎯 作答毛概错题集（${{mao.wrongCount}} 题）</a>
        <a class="btn btn-primary btn-block" href="#quiz" onclick="setSubject('xi')">📘 作答习概题库（${{xi.total}} 题）</a>
        <a class="btn btn-primary btn-block" href="#wrong" onclick="setSubject('xi')">🎯 作答习概错题集（${{xi.wrongCount}} 题）</a>
        <a class="btn btn-outline btn-block" href="#stats">📊 查看各题作答情况</a>
        <a class="btn btn-outline btn-block" href="#history">📋 查看作答记录</a>
      </div>
    </div>
    <div class="card" style="text-align:center;">
      <p style="color:var(--c-text-light);font-size:.85rem;margin-bottom:10px;">数据保存在浏览器本地存储中，备份文件为同目录下的 <code>${{BACKUP_FILENAME}}</code></p>
      <div class="btn-group" style="justify-content:center;">
        <button class="btn btn-outline btn-sm" onclick="exportData()">📥 导出备份</button>
        <button class="btn btn-outline btn-sm" onclick="autoLoadBackup()">🔄 加载备份</button>
        <button class="btn btn-outline btn-sm" onclick="document.getElementById('importFile').click()">📤 选择文件导入</button>
        <button class="btn btn-danger btn-sm" onclick="clearAllData()">🗑 清空记录</button>
      </div>
      <input type="file" id="importFile" accept=".json" style="display:none;" onchange="importData(event)">
    </div>
  `;
}}

function setSubject(s){{currentSubject=s;}}

function clearAllData(){{
  if(confirm('确定要清空所有本机记录吗？\\n\\n这将删除：\\n- 所有作答统计\\n- 所有错题记录\\n- 所有作答历史\\n\\n此操作不可恢复！')){{
    localStorage.removeItem(STATS_KEY);localStorage.removeItem(HISTORY_KEY);render();
  }}
}}

function exportData(){{
  const d={{exportedAt:new Date().toLocaleString('zh-CN',{{hour12:false}}),stats:loadStats(),history:loadHistory()}};
  const j=JSON.stringify(d,null,2);
  const b=new Blob([j],{{type:'application/json'}});
  const u=URL.createObjectURL(b);
  const a=document.createElement('a');a.href=u;a.download=BACKUP_FILENAME;
  document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(u);
}}

async function autoLoadBackup(){{
  try{{
    const r=await fetch('./'+BACKUP_FILENAME);
    if(!r.ok){{alert('❌ 未找到备份文件');return}}
    const d=await r.json();
    if(!d.stats||!d.history){{alert('❌ 文件格式不正确');return}}
    if(!confirm('确定要恢复备份吗？当前记录将被覆盖！'))return;
    saveStats(d.stats);saveHistory(d.history);alert('✅ 备份恢复成功！');render();
  }}catch(e){{alert('❌ 加载失败：'+e.message)}}
}}

async function autoLoadOnStartup(){{
  const s=loadStats(),h=loadHistory();
  if(Object.keys(s).length>0||h.length>0)return;
  try{{const r=await fetch('./'+BACKUP_FILENAME);if(!r.ok)return;
    const d=await r.json();if(d.stats&&d.history){{saveStats(d.stats);saveHistory(d.history);}}
  }}catch(e){{}}
}}

function importData(event){{
  const f=event.target.files[0];if(!f)return;
  if(!confirm('确定要恢复备份吗？当前记录将被覆盖！')){{event.target.value='';return}}
  const r=new FileReader();
  r.onload=function(e){{try{{const d=JSON.parse(e.target.result);
    if(d.stats&&d.history){{saveStats(d.stats);saveHistory(d.history);alert('✅ 备份恢复成功！');render()}}
    else{{alert('❌ 文件格式不正确')}}
  }}catch(err){{alert('❌ 无法解析该文件')}}}};
  r.readAsText(f);event.target.value='';
}}

// ========== QUIZ ==========
function renderQuiz(app){{
  const qs=qsBySubject(currentSubject);
  const singles=shuffle(qs.filter(q=>q.type==='single'));
  const multis=shuffle(qs.filter(q=>q.type==='multiple'));
  const judges=shuffle(qs.filter(q=>q.type==='judge'));
  quizQuestions=[...singles,...multis,...judges];
  quizIndex=0;quizAnswered={{}};
  renderQuizQuestion(app);
}}

function renderWrong(app){{
  const stats=loadStats();
  const wrongIds=[];
  for(const q of qsBySubject(currentSubject)){{
    const s=stats[q.id];
    if(s&&s.attempts>0&&s.wrongRate>30)wrongIds.push(q.id);
  }}
  if(wrongIds.length===0){{
    app.innerHTML=`<div class="card"><h2>🎯 错题集</h2><div class="empty"><div class="icon">🎉</div><p>太棒了！当前学科没有错误率超过30%的题目。</p><a class="btn btn-primary" href="#home" style="margin-top:16px;">返回首页</a></div></div>`;return;
  }}
  const wSingles=shuffle(wrongIds.filter(id=>id.startsWith('single-')).map(id=>getQ(id)));
  const wMultis=shuffle(wrongIds.filter(id=>id.startsWith('multiple-')).map(id=>getQ(id)));
  const wJudges=shuffle(wrongIds.filter(id=>id.startsWith('judge-')).map(id=>getQ(id)));
  quizQuestions=[...wSingles,...wMultis,...wJudges];
  quizIndex=0;quizAnswered={{}};
  renderQuizQuestion(app);
}}

function renderQuizQuestion(app){{
  if(quizIndex>=quizQuestions.length){{renderQuizComplete(app);return}}
  const q=quizQuestions[quizIndex],total=quizQuestions.length;
  const progress=Math.round(((quizIndex+1)/total)*100);
  const isXi=q.subject==='xi';
  const barClass=isXi?'xi':'mao';
  const tLabel=typeLabel(q.type),tTag=typeTagClass(q.type);
  const keyHint='⌨ 1-4 选项 · Enter 提交 · ← → 翻题';

  let optionsHTML='';
  if(q.type==='judge'){{
    optionsHTML=`
      <button class="option" data-label="true" onclick="selectJudgeOption(this,'true')"><span class="option-label">✓</span>正确</button>
      <button class="option" data-label="false" onclick="selectJudgeOption(this,'false')"><span class="option-label">✗</span>错误</button>`;
  }}else if(q.type==='single'){{
    for(const o of q.options){{
      optionsHTML+=`<button class="option" data-label="${{o.label}}" onclick="selectSingleOption(this)"><span class="option-label">${{o.label}}</span>${{o.text}}</button>`;
    }}
  }}else{{
    for(const o of q.options){{
      optionsHTML+=`<label class="option" data-label="${{o.label}}"><input type="checkbox" value="${{o.label}}" onchange="toggleMultiOption(this)"><span class="check-mark">${{o.label}}</span>${{o.text}}</label>`;
    }}
  }}

  const already=quizAnswered[q.id];
  const subjectTag=isXi?'<span class="tag tag-xi">习概</span>':'<span class="tag tag-mao">毛概</span>';

  app.innerHTML=`
    <div class="card ${{isXi?'':'mao-card'}}">
      <div class="quiz-progress">
        <span>${{subjectTag}} <span class="tag ${{tTag}}">${{tLabel}}</span> 第 ${{q.sourceOrder}} 题</span>
        <span>${{quizIndex+1}} / ${{total}}</span>
      </div>
      <div class="progress-bar ${{barClass}}"><div class="fill" style="width:${{progress}}%"></div></div>
      <div class="hint-text">${{keyHint}}</div>
      <div class="question-block"><div class="question-text">${{q.question}}</div></div>
      <div class="options" id="optionsContainer">${{optionsHTML}}</div>
      <div class="feedback" id="feedback"></div>
      <div class="quiz-nav" id="quizNav">
        ${{quizIndex>0?`<button class="btn btn-outline" onclick="prevQuestion()">← 上一题</button>`:'<span style="width:90px;display:inline-block;"></span>'}}
        ${{!already?`<button class="btn ${{isXi?'btn-primary':'btn-mao'}}" onclick="submitAnswer('${{q.id}}')">✅ 提交本题</button>`:''}}
        ${{already?'<span style="font-size:.85rem;color:var(--c-text-light);">本题已作答</span>':''}}
        ${{quizIndex<total-1?`<button class="btn btn-outline" onclick="nextQuestion()">下一题 →</button>`:`<button class="btn btn-outline" onclick="nextQuestion()">完成 →</button>`}}
      </div>
    </div>`;
}}

function selectSingleOption(btnEl){{
  const c=document.getElementById('optionsContainer');
  c.querySelectorAll('.option').forEach(el=>el.classList.remove('selected'));
  btnEl.classList.add('selected');
}}

function selectJudgeOption(btnEl,val){{
  const c=document.getElementById('optionsContainer');
  c.querySelectorAll('.option').forEach(el=>el.classList.remove('selected'));
  btnEl.classList.add('selected');
}}

function submitAnswer(qid){{
  const q=getQ(qid);
  if(quizAnswered[qid])return;
  if(q.type==='single')submitSingle(qid);
  else if(q.type==='multiple')submitMultiple(qid);
  else if(q.type==='judge')submitJudge(qid);
}}

function submitSingle(qid){{
  if(quizAnswered[qid])return;
  const sel=document.querySelector('#optionsContainer .option.selected');
  if(!sel){{alert('请先选择一个选项');return}}
  quizAnswered[qid]=true;
  const label=sel.getAttribute('data-label'),q=getQ(qid),isCorrect=q.answer===label;
  markAndFeedback(qid,label,isCorrect,q.answer);
  recordAttempt(q,label,isCorrect);
}}

function toggleMultiOption(cb){{
  const l=cb.closest('.option');
  l.classList.toggle('selected',cb.checked);
}}

function submitMultiple(qid){{
  if(quizAnswered[qid])return;
  quizAnswered[qid]=true;
  const q=getQ(qid),c=document.getElementById('optionsContainer');
  const checked=[];c.querySelectorAll('input[type="checkbox"]:checked').forEach(cb=>checked.push(cb.value));
  checked.sort();const ua=checked.join('、')||'(未选)';
  const ca=q.answer.split('、').map(s=>s.trim()).sort(),cs=ca.join('、');
  const isCorrect=checked.length===ca.length&&checked.every((v,i)=>v===ca[i]);
  c.querySelectorAll('.option').forEach(el=>el.classList.add('disabled'));
  c.querySelectorAll('input[type="checkbox"]').forEach(cb=>cb.disabled=true);
  c.querySelectorAll('.option').forEach(el=>{{
    const lbl=el.getAttribute('data-label');
    if(ca.includes(lbl))el.classList.add('correct');
    else if(checked.includes(lbl))el.classList.add('wrong');
  }});
  showFeedback(isCorrect,isCorrect?'✅ 回答正确！':`❌ 回答错误。正确答案是 <strong>${{cs}}</strong>。你的答案：${{ua}}`);
  updateQuizNav();
  recordAttempt(q,ua,isCorrect);
}}

function submitJudge(qid){{
  if(quizAnswered[qid])return;
  quizAnswered[qid]=true;
  const sel=document.querySelector('#optionsContainer .option.selected');
  if(!sel){{alert('请先选择正确或错误');return}}
  const val=sel.getAttribute('data-label'),q=getQ(qid);
  const userAns=val==='true'?'正确':'错误';
  const isCorrect=userAns===q.answer;
  const c=document.getElementById('optionsContainer');
  c.querySelectorAll('.option').forEach(el=>el.classList.add('disabled'));
  const correctOpt=c.querySelector(`[data-label="${{q.answer==='正确'?'true':'false'}}"]`);
  if(correctOpt)correctOpt.classList.add('correct');
  if(!isCorrect)sel.classList.add('wrong');else sel.classList.add('correct');
  showFeedback(isCorrect,'✅ 回答正确！',`❌ 回答错误。正确答案是 <strong>${{q.answer}}</strong>。`);
  updateQuizNav();
  recordAttempt(q,userAns,isCorrect);
}}

function markAndFeedback(qid,label,isCorrect,answer){{
  const c=document.getElementById('optionsContainer');
  c.querySelectorAll('.option').forEach(el=>el.classList.add('disabled'));
  const sel=c.querySelector(`[data-label="${{label}}"]`);
  if(sel)sel.classList.add(isCorrect?'correct':'wrong');
  const cor=c.querySelector(`[data-label="${{answer}}"]`);
  if(cor&&cor!==sel)cor.classList.add('correct');
  showFeedback(isCorrect,isCorrect?'✅ 回答正确！':`❌ 回答错误。正确答案是 <strong>${{answer}}</strong>。`);
  updateQuizNav();
}}

function showFeedback(isCorrect,correctMsg,wrongMsg){{
  const fb=document.getElementById('feedback');
  fb.className='feedback show '+(isCorrect?'correct-fb':'wrong-fb');
  fb.innerHTML=isCorrect?correctMsg:(wrongMsg||correctMsg);
}}

function updateQuizNav(){{
  document.getElementById('quizNav').innerHTML=`
    ${{quizIndex>0?`<button class="btn btn-outline" onclick="prevQuestion()">← 上一题</button>`:'<span style="width:90px;display:inline-block;"></span>'}}
    <span style="font-size:.85rem;color:var(--c-text-light);">本题已作答</span>
    ${{quizIndex<quizQuestions.length-1?`<button class="btn btn-outline" onclick="nextQuestion()">下一题 →</button>`:`<button class="btn btn-outline" onclick="nextQuestion()">完成 →</button>`}}`;
}}

function recordAttempt(q,userAnswer,isCorrect){{
  const stats=loadStats(),sid=q.id;
  if(!stats[sid])stats[sid]={{attempts:0,correct:0,wrong:0,accuracy:0,wrongRate:0}};
  stats[sid].attempts++;
  if(isCorrect)stats[sid].correct++;else stats[sid].wrong++;
  const t=stats[sid].attempts;
  stats[sid].accuracy=Math.round(stats[sid].correct/t*100);
  stats[sid].wrongRate=Math.round(stats[sid].wrong/t*100);
  saveStats(stats);
  const history=loadHistory();
  history.unshift({{
    time:new Date().toLocaleString('zh-CN',{{hour12:false}}),
    id:q.id,sourceOrder:q.sourceOrder,subject:q.subject,
    type:q.type==='single'?'单选':q.type==='multiple'?'多选':'判断',
    userAnswer:userAnswer,correctAnswer:q.answer,isCorrect:isCorrect
  }});
  saveHistory(history);
}}

function nextQuestion(){{quizIndex++;renderQuizQuestion(document.getElementById('app'))}}
function prevQuestion(){{if(quizIndex>0){{quizIndex--;renderQuizQuestion(document.getElementById('app'))}}}}

function renderQuizComplete(app){{
  let sessionCorrect=0,sessionTotal=0;
  const history=loadHistory();
  for(const qid of Object.keys(quizAnswered)){{
    if(quizAnswered[qid]){{sessionTotal++;const last=history.find(h=>h.id===qid);if(last&&last.isCorrect)sessionCorrect++;}}
  }}
  const isXi=currentSubject==='xi';
  app.innerHTML=`
    <div class="card" style="text-align:center;">
      <h2>🎉 本轮作答完成！</h2>
      <div class="stat-grid" style="margin:20px 0;">
        <div class="stat-item"><div class="num">${{sessionTotal}}</div><div class="label">本轮作答</div></div>
        <div class="stat-item"><div class="num">${{sessionCorrect}}</div><div class="label">本轮正确</div></div>
        <div class="stat-item"><div class="num">${{sessionTotal>0?Math.round(sessionCorrect/sessionTotal*100):0}}%</div><div class="label">本轮正确率</div></div>
      </div>
      <div class="btn-group" style="justify-content:center;margin-top:20px;">
        <a class="btn ${{isXi?'btn-primary':'btn-mao'}}" href="#quiz">🔄 重新作答</a>
        <a class="btn btn-outline" href="#wrong">🎯 错题集</a>
        <a class="btn btn-outline" href="#home">🏠 返回首页</a>
      </div>
    </div>`;
}}

// ========== STATS ==========
function renderStats(app){{
  const stats=loadStats();
  let currentStatsSubject='mao';
  
  function buildTable(qs){{
    let rows='';
    for(const q of qs){{
      const s=stats[q.id],attempts=s?s.attempts:0,correct=s?s.correct:0,wrong=s?s.wrong:0;
      const accuracy=s?s.accuracy:'-',wrongRate=s?s.wrongRate:'-';
      let ac='';if(typeof accuracy==='number'){{if(accuracy>=80)ac='acc-high';else if(accuracy>=50)ac='acc-mid';else ac='acc-low'}}
      let wc='';if(typeof wrongRate==='number'){{if(wrongRate>50)wc='acc-low';else if(wrongRate>30)wc='acc-mid'}}
      rows+=`<tr><td>${{q.sourceOrder}}</td><td><span class="tag ${{typeTagClass(q.type)}}">${{typeLabel(q.type)}}</span></td><td class="text-left">${{q.question.substring(0,60)}}…</td><td>${{q.answer}}</td><td>${{attempts}}</td><td>${{correct}}</td><td>${{wrong}}</td><td class="${{ac}}">${{accuracy}}${{typeof accuracy==='number'?'%':''}}</td><td class="${{wc}}">${{wrongRate}}${{typeof wrongRate==='number'?'%':''}}</td></tr>`;
    }}
    return rows;
  }}

  function renderTable(subj){{
    const qs=qsBySubject(subj);
    const singles=qs.filter(q=>q.type==='single'),multis=qs.filter(q=>q.type==='multiple'),judges=qs.filter(q=>q.type==='judge');
    const subjectName=subj==='mao'?'毛泽东思想':'习近平思想';
    let html=`<h2>📊 ${{subjectName}} 作答统计</h2>`;
    const colHead='<tr><th>#</th><th>类型</th><th>题干</th><th>答案</th><th>作答</th><th>正确</th><th>错误</th><th>正确率</th><th>错误率</th></tr>';
    html+=`<h3 style="margin-top:12px;">单选题（${{singles.length}} 题）</h3><div class="table-wrap"><table><thead>${{colHead}}</thead><tbody>${{buildTable(singles)}}</tbody></table></div>`;
    html+=`<h3 style="margin-top:16px;">多选题（${{multis.length}} 题）</h3><div class="table-wrap"><table><thead>${{colHead}}</thead><tbody>${{buildTable(multis)}}</tbody></table></div>`;
    if(judges.length>0)html+=`<h3 style="margin-top:16px;">判断题（${{judges.length}} 题）</h3><div class="table-wrap"><table><thead>${{colHead}}</thead><tbody>${{buildTable(judges)}}</tbody></table></div>`;
    return html;
  }}

  app.innerHTML=`
    <div class="subject-tabs" style="margin-bottom:12px;">
      <button class="subject-tab mao-tab active" onclick="switchStatsTab('mao')">📕 毛泽东思想</button>
      <button class="subject-tab" onclick="switchStatsTab('xi')">📘 习近平思想</button>
    </div>
    <div class="card"><div id="statsContent">${{renderTable('mao')}}</div></div>
    <div style="text-align:center;padding:10px;"><a class="btn btn-outline" href="#home">🏠 返回首页</a></div>`;
}}

function switchStatsTab(subj){{
  document.querySelectorAll('.subject-tab').forEach((el,i)=>{{
    el.classList.toggle('active',(i===0&&subj==='mao')||(i===1&&subj==='xi'));
  }});
  const stats=loadStats();
  function buildTable(qs){{
    let rows='';
    for(const q of qs){{
      const s=stats[q.id],attempts=s?s.attempts:0,correct=s?s.correct:0,wrong=s?s.wrong:0;
      const accuracy=s?s.accuracy:'-',wrongRate=s?s.wrongRate:'-';
      let ac='';if(typeof accuracy==='number'){{if(accuracy>=80)ac='acc-high';else if(accuracy>=50)ac='acc-mid';else ac='acc-low'}}
      let wc='';if(typeof wrongRate==='number'){{if(wrongRate>50)wc='acc-low';else if(wrongRate>30)wc='acc-mid'}}
      rows+=`<tr><td>${{q.sourceOrder}}</td><td><span class="tag ${{typeTagClass(q.type)}}">${{typeLabel(q.type)}}</span></td><td class="text-left">${{q.question.substring(0,60)}}…</td><td>${{q.answer}}</td><td>${{attempts}}</td><td>${{correct}}</td><td>${{wrong}}</td><td class="${{ac}}">${{accuracy}}${{typeof accuracy==='number'?'%':''}}</td><td class="${{wc}}">${{wrongRate}}${{typeof wrongRate==='number'?'%':''}}</td></tr>`;
    }}
    return rows;
  }}
  const qs=qsBySubject(subj);
  const singles=qs.filter(q=>q.type==='single'),multis=qs.filter(q=>q.type==='multiple'),judges=qs.filter(q=>q.type==='judge');
  const subjectName=subj==='mao'?'毛泽东思想':'习近平思想';
  const colHead='<tr><th>#</th><th>类型</th><th>题干</th><th>答案</th><th>作答</th><th>正确</th><th>错误</th><th>正确率</th><th>错误率</th></tr>';
  let html=`<h2>📊 ${{subjectName}} 作答统计</h2>`;
  html+=`<h3 style="margin-top:12px;">单选题（${{singles.length}} 题）</h3><div class="table-wrap"><table><thead>${{colHead}}</thead><tbody>${{buildTable(singles)}}</tbody></table></div>`;
  html+=`<h3 style="margin-top:16px;">多选题（${{multis.length}} 题）</h3><div class="table-wrap"><table><thead>${{colHead}}</thead><tbody>${{buildTable(multis)}}</tbody></table></div>`;
  if(judges.length>0)html+=`<h3 style="margin-top:16px;">判断题（${{judges.length}} 题）</h3><div class="table-wrap"><table><thead>${{colHead}}</thead><tbody>${{buildTable(judges)}}</tbody></table></div>`;
  document.getElementById('statsContent').innerHTML=html;
}}

// ========== HISTORY ==========
let historySubject='all';

function renderHistory(app){{
  const history=loadHistory();
  if(history.length===0){{
    app.innerHTML=`<div class="card"><h2>📋 作答记录</h2><div class="empty"><div class="icon">📭</div><p>暂无作答记录。</p><a class="btn btn-primary" href="#home" style="margin-top:16px;">返回首页</a></div></div>`;return;
  }}
  const filtered=historySubject==='all'?history:history.filter(h=>h.subject===historySubject);
  let rows='';
  for(const h of filtered){{
    const icon=h.isCorrect?'✅':'❌';
    const subjTag=h.subject==='mao'?'<span class="tag tag-mao">毛概</span>':'<span class="tag tag-xi">习概</span>';
    rows+=`<tr><td>${{h.time}}</td><td>${{subjTag}}</td><td>${{h.sourceOrder}}</td><td><span class="tag ${{h.type==='单选'?'tag-single':h.type==='多选'?'tag-multiple':'tag-judge'}}">${{h.type}}</span></td><td>${{h.userAnswer}}</td><td>${{h.correctAnswer}}</td><td>${{icon}}</td></tr>`;
  }}

  app.innerHTML=`
    <div class="card">
      <h2>📋 作答记录（共 ${{filtered.length}} 条）</h2>
      <div class="filter-bar">
        <button class="btn ${{historySubject==='all'?'btn-primary':'btn-outline'}} btn-sm" onclick="setHistoryFilter('all')">全部</button>
        <button class="btn ${{historySubject==='mao'?'btn-mao':'btn-outline'}} btn-sm" onclick="setHistoryFilter('mao')">毛概</button>
        <button class="btn ${{historySubject==='xi'?'btn-primary':'btn-outline'}} btn-sm" onclick="setHistoryFilter('xi')">习概</button>
      </div>
      <div class="table-wrap">
        <table><thead><tr><th>时间</th><th>学科</th><th>题号</th><th>类型</th><th>你的答案</th><th>正确答案</th><th>结果</th></tr></thead>
        <tbody>${{rows}}</tbody></table>
      </div>
      <div style="text-align:center;margin-top:16px;">
        <button class="btn btn-danger btn-sm" onclick="clearHistory()">🗑 清空作答记录</button>
      </div>
    </div>
    <div style="text-align:center;padding:10px;"><a class="btn btn-outline" href="#home">🏠 返回首页</a></div>`;
}}

function setHistoryFilter(s){{historySubject=s;renderHistory(document.getElementById('app'))}}
function clearHistory(){{if(confirm('确定要清空所有作答记录吗？（不影响统计数据）')){{localStorage.setItem(HISTORY_KEY,JSON.stringify([]));render()}}}}

// ========== KEYBOARD ==========
document.addEventListener('keydown',(e)=>{{
  const page=getPage();
  if(page!=='quiz'&&page!=='wrong')return;
  if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA')return;
  if(e.key==='ArrowLeft'||e.key==='ArrowUp'){{e.preventDefault();if(quizIndex>0)prevQuestion()}}
  else if(e.key==='ArrowRight'||e.key==='ArrowDown'){{e.preventDefault();if(quizIndex<quizQuestions.length-1)nextQuestion()}}
  else if(e.key==='Enter'){{e.preventDefault();const q=quizQuestions[quizIndex];if(!quizAnswered[q.id])submitAnswer(q.id)}}
  else if(e.key>='1'&&e.key<='4'){{
    e.preventDefault();const q=quizQuestions[quizIndex];if(quizAnswered[q.id])return;
    const idx=parseInt(e.key)-1,c=document.getElementById('optionsContainer');if(!c)return;
    const opts=c.querySelectorAll('.option');if(idx>=opts.length)return;
    const t=opts[idx];
    if(q.type==='single'||q.type==='judge'){{
      if(t.classList.contains('selected'))t.classList.remove('selected');
      else{{c.querySelectorAll('.option').forEach(el=>el.classList.remove('selected'));t.classList.add('selected');}}
    }}else{{
      const cb=t.querySelector('input[type="checkbox"]');if(cb){{cb.checked=!cb.checked;cb.dispatchEvent(new Event('change',{{bubbles:true}}));}}
    }}
  }}
}});

// ========== INIT ==========
document.addEventListener('DOMContentLoaded',()=>{{autoLoadOnStartup().then(()=>render())}});
</script>
</body>
</html>'''

# Write the HTML
output_path = os.path.join(script_dir, '习思想刷题.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

size = os.path.getsize(output_path)
print(f'HTML written: {output_path} ({size} bytes)')
