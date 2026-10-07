from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import sys
w=Path(__file__).resolve().parents[2]
public='--public' in sys.argv
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='chrome',headless=True)
 for width,height in [(390,844),(360,640),(1280,900)]:
  c=b.new_context(viewport={'width':width,'height':height},service_workers='block')
  c.add_init_script("""const native=fetch;window.fetch=(u,o)=>String(u).includes('tail8fd071')?Promise.resolve(new Response('{"ok":true,"entries":{},"revision":0,"acceptedKeys":[]}')):native(u,o);""")
  p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  if not public:
   def route(r):
    path=urlparse(r.request.url).path.lstrip('/')
    f=w/path
    if f.is_dir():f=f/'index.html'
    if not f.exists():r.abort();return
    r.fulfill(body=f.read_bytes(),content_type={'.js':'application/javascript','.html':'text/html','.json':'application/json','.css':'text/css'}.get(f.suffix,'application/octet-stream'))
   p.route('https://adrianxds-ads.github.io/**',route)
  p.goto('https://adrianxds-ads.github.io/adaptive-keyword-speaking/?audit=101',wait_until='networkidle')
  p.locator('#startBtn').click()
  count=p.evaluate('QUESTIONS.length')
  # Composition must preserve the exact text until explicit checking.
  full=p.evaluate("current().secondBefore+' '+expectedVariants(current())[0]+' '+current().secondAfter")
  p.locator('#answer').fill(full)
  p.locator('#answer').dispatch_event('compositionstart')
  p.locator('#answer').dispatch_event('compositionend')
  mutated=p.locator('#answer').input_value()!=full
  print('composition mutated',mutated,'width',width,flush=True)
  if '--baseline' in sys.argv:continue
  assert not mutated
  assert p.locator('#answer').evaluate('(e)=>e.tagName')=='TEXTAREA'
  # Correct every reference solution and full sentence in the bank.
  check=p.evaluate("""()=>QUESTIONS.flatMap(q=>expectedVariants(q).flatMap(v=>{
   const full=[q.secondBefore,v,q.secondAfter].join(' ');
   const x=parseFullSentence(full,q);
   return scoreTransformation(v,q).points!==2||!x.full||scoreTransformation(x.gap,q).points!==2?[{id:q._qid,v,full,parsed:x}]:[];
  }))""")
  assert not check,check
  p.locator('#checkBtn').click()
  assert '2/2' in p.locator('#feedback').inner_text()
  p.locator('#checkBtn').click(force=True,timeout=1000) if not p.locator('#checkBtn').is_disabled() else None
  assert p.evaluate('session.results.length')==1
  p.locator('#nextBtn').click()
  assert p.locator('#answer').evaluate('(e)=>e.dataset.voice')=='0'
  for i in range(14):
   p.locator('#answer').fill('totally wrong')
   p.locator('#checkBtn').click()
   assert '0/2' in p.locator('#feedback').inner_text()
   p.locator('#nextBtn').click()
  assert p.locator('#review .review-row').count()==14
  saved=p.evaluate("JSON.parse(localStorage.getItem(STATS_KEY))")
  assert len(saved['sessions'])==1 and saved['sessions'][0]['correct']==2
  p.reload(wait_until='networkidle')
  assert p.evaluate("JSON.parse(localStorage.getItem(STATS_KEY)).sessions.length")==1
  p.locator('#startBtn').click()
  long='would have been able to '+'a long answer '*12
  p.locator('#answer').fill(long)
  p.locator('#answer').dispatch_event('input')
  assert p.locator('#answer').evaluate('(e)=>e.scrollHeight<=e.clientHeight+2')
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not errors,errors
  print('PASS',width,'bank',count,'composition, scoring, 15 transitions, persistence, multiline, overflow, console',flush=True)
  c.close()
 b.close()
