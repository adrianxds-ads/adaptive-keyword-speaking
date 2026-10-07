from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import sys,json
w=Path(__file__).resolve().parents[2];baseline='--baseline' in sys.argv;public='--public' in sys.argv
mock="""class VoiceMock {start(){this.onstart?.()}stop(){this.onend?.()} emit(text,final=true){const result=[{transcript:text}];result.isFinal=final;this.onresult?.({results:[result],resultIndex:0});} } window.SpeechRecognition=VoiceMock;"""
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='chrome',headless=True)
 for width,height in [(390,844),(360,640),(1280,900)]:
  c=b.new_context(viewport={'width':width,'height':height},service_workers='block')
  c.add_init_script(mock)
  c.add_init_script("""const native=fetch;window.fetch=(u,o)=>String(u).includes('tail8fd071')?Promise.resolve(new Response('{"ok":true,"entries":{},"revision":0,"acceptedKeys":[]}')):native(u,o);""")
  p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  if not public:
   def route(r):
    f=w/urlparse(r.request.url).path.lstrip('/')
    if f.is_dir():f=f/'index.html'
    if not f.exists():r.abort();return
    r.fulfill(body=f.read_bytes(),content_type={'.js':'application/javascript','.html':'text/html','.css':'text/css','.json':'application/json'}.get(f.suffix,'application/octet-stream'))
   p.route('https://adrianxds-ads.github.io/**',route)
  p.goto('https://adrianxds-ads.github.io/adaptive-keyword-speaking/?voice-audit=103',wait_until='networkidle')
  p.locator('#startBtn').click()
  font=p.locator('#answer').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')
  cases=p.evaluate("""()=>{
 const q={secondBefore:'I ',secondAfter:' in Barcelona.',keyword:'BEEN',answers:['have been living']};
 return ['have been living','I have been living','have been living in Barcelona','I have been living in Barcelona'].map(text=>({text,p:parseFullSentence(text,q)}));
 }""")
  print('width',width,'font',font,'cases',cases,flush=True)
  if baseline:continue
  assert font>=30,font
  assert all(v['p']['gap']=='have been living' for v in cases),cases
  assert not cases[0]['p']['full']
  check=p.evaluate("""()=>{
 const failed=[];
 for(const q of QUESTIONS)for(const v of expectedVariants(q)){
  for(const text of [v,[q.secondBefore,v].join(' '),[v,q.secondAfter].join(' '),[q.secondBefore,v,q.secondAfter].join(' ')]){
   const result=parseFullSentence(text,q);
   if(scoreTransformation(result.gap,q).points!==2)failed.push({id:q._qid,v,text,result});
  }
 }
 return failed;
 }""")
  assert not check,check
  p.evaluate("""()=>{
 const q={_qid:'test-voice',n:25,first:'I started living here three years ago.',secondBefore:'I ',secondAfter:' in Barcelona.',keyword:'BEEN',answers:['have been living']};
 session.questions[0]=q;renderQuestion();
 }""")
  p.locator('#micBtn').click()
  p.evaluate("recognition.emit('I have been living in Barcelona',false)")
  assert p.locator('#answer').input_value()=='have been living'
  assert p.locator('#secondBefore .recognized').inner_text().strip()=='I'
  assert p.locator('#secondAfter .recognized').inner_text().strip()=='in Barcelona'
  assert p.evaluate('session.results.length')==0
  p.evaluate("recognition.emit('I have been living in Barcelona',true);recognition.onend()")
  p.locator('#checkBtn').click()
  assert '2/2' in p.locator('#feedback').inner_text()
  assert p.evaluate('session.results[0].usedVoice')
  p.locator('#nextBtn').click()
  # Wrong response remains wrong, including extra gap words, even with recognized context.
  extra=p.evaluate("""()=>{
 const q={secondBefore:'The heavy snow ',secondAfter:' for a couple of days.',keyword:'LED',answers:['led to schools being closed']};
 const wrong='led the schools closed unexpectedly again';
 const p=parseFullSentence('The heavy snow '+wrong+' for a couple of days',q);
 return {gap:p.gap,points:scoreTransformation(p.gap,q).points};
 }""")
  assert extra['gap']=='led the schools closed unexpectedly again' and extra['points']==0,extra
  contracted=p.evaluate("""()=>{
 const q={secondBefore:"I don't ",secondAfter:' him.',keyword:'AS',answers:['speak as well as']};
 return parseFullSentence('I do not speak as well as him',q);
 }""")
  assert contracted['gap']=='speak as well as',contracted
  # Gboard composition previews recognized fixed words but preserves the IME text.
  full=p.evaluate("current().secondBefore+' '+expectedVariants(current())[0]+' '+current().secondAfter")
  p.locator('#answer').fill(full)
  p.locator('#answer').dispatch_event('compositionstart')
  p.locator('#answer').dispatch_event('input')
  p.locator('#answer').dispatch_event('compositionend')
  assert p.locator('#answer').input_value()==full
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not errors,errors
  p.screenshot(path=str(w/('keyword-103-'+str(width)+'.png')),full_page=True)
  print('PASS',width,'all bank variants in 4 speech forms, blue context, live microphone, no auto scoring, Gboard stable, extra words retained',flush=True)
  c.close()
 b.close()
