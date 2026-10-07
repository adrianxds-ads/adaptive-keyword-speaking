from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
w=Path(__file__).resolve().parents[2]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='chrome',headless=True)
 c=b.new_context(viewport={'width':390,'height':844},service_workers='block')
 c.add_init_script("""window.fetch=()=>Promise.resolve(new Response('{"ok":true,"entries":{},"revision":0,"acceptedKeys":[]}'));""")
 p=c.new_page()
 def route(r):
  f=w/urlparse(r.request.url).path.lstrip('/')
  if f.is_dir():f=f/'index.html'
  if not f.exists():r.abort();return
  r.fulfill(body=f.read_bytes(),content_type={'.js':'application/javascript','.html':'text/html'}.get(f.suffix,'application/octet-stream'))
 p.route('https://adrianxds-ads.github.io/**',route)
 p.goto('https://adrianxds-ads.github.io/adaptive-keyword-speaking/',wait_until='networkidle')
 p.locator('#startBtn').click()
 out=p.evaluate("""()=>{
 const q=QUESTIONS.find(q=>q.keyword==='LED');
 const wrong='led the schools closed';
 const extra='led to the schools being closed unexpectedly';
 const full=[q.secondBefore,extra,q.secondAfter].join(' ');
 if(parseFullSentence(full,q).gap!==extra)throw Error('Truncated incorrect full phrase');
 if(scoreTransformation(parseFullSentence(full,q).gap,q).reason!=='word-count')throw Error('Extra words ignored');
 return {wrong:scoreTransformation(wrong,q),extra:parseFullSentence(full,q)};
 }""")
 print(out)
 p.locator('#answer').fill('typing in progress')
 p.locator('#answer').dispatch_event('compositionstart')
 p.locator('#answer').dispatch_event('keydown',{'key':'Enter','isComposing':True})
 assert p.evaluate('session.results.length')==0
 p.locator('#answer').dispatch_event('compositionend')
 p.locator('#answer').fill(p.evaluate('expectedVariants(current())[0]'))
 p.locator('#checkBtn').click()
 p.locator('#nextBtn').click()
 p.locator('#answer').fill(p.evaluate('expectedVariants(current())[0]'))
 p.locator('#checkBtn').click()
 assert 'Racha de 2' in p.locator('#feedback').inner_text()
 p.locator('#nextBtn').click()
 p.locator('#answer').fill('led to the schools being closed')
 p.locator('#answer').dispatch_event('input')
 p.screenshot(path=str(w/'keyword-101-mobile.png'),full_page=True)
 print('PASS incorrect full-sentence retention, word count, composing Enter, immediate streak')
 b.close()
