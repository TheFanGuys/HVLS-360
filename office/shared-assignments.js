/* Shared public metadata only. GitHub Issues remains authoritative. */
(function (root) {
 'use strict';
 const api='https://api.github.com/repos/TheFanGuys/HVLS-360/issues';
 function category(issue) {
  if (issue.pull_request || issue.state !== 'open') return null;
  if (/^\[HVLS-\d+\]/.test(issue.title)) return 'article';
  if (/^\[OPS-\d+\]/.test(issue.title)) return 'operations';
  if (/^\[(?:Research pitch|COO Research)\]/.test(issue.title)) return 'research';
  return null;
 }
 function field(body,name) {
  const line=(body||'').split('\n').find(s=>s.startsWith('**'+name+':**'));
  return line ? line.slice(name.length+5).trim() : '';
 }
 async function read(transport=root.fetch) {
  const issues=[];
  for(let page=1;page<=10;page++) {
   const response=await transport(api+'?state=open&per_page=100&page='+page,{cache:'no-store',headers:{Accept:'application/vnd.github+json'}});
   if(!response.ok) throw Error('GitHub returned HTTP '+response.status+'. Open the COO summary for the shared records.');
   const batch=await response.json();
   if(!Array.isArray(batch)) throw Error('Invalid assignment response');
   issues.push(...batch.filter(x=>category(x)));
   if(batch.length<100) return issues;
  }
  throw Error('Assignment list exceeded page limit; use the full GitHub board.');
 }
 root.HVLSSharedAssignments={category,field,read};
 if(!root.document) return;
 const $=id=>document.getElementById(id);let issues=[];
 function render() {
  const host=$('assignments');host.replaceChildren();
  const query=$('search').value.toLowerCase(),kind=$('kind').value;
  const shown=issues.filter(x=>(kind==='all'||category(x)===kind)&&(x.title+' '+x.body).toLowerCase().includes(query));
  for(const issue of shown) {
   const box=document.createElement('article');box.className='card';
   const h=document.createElement('h2'),link=document.createElement('a');
   link.href='https://github.com/TheFanGuys/HVLS-360/issues/'+Number(issue.number);link.textContent=issue.title;h.append(link);
   const status=document.createElement('span');status.className='badge';status.textContent=field(issue.body,'Status')||field(issue.body,'State')||'Open — see latest handoff';
   box.append(h,status);
   for(const [label,value] of [['Owner',field(issue.body,'Owner')||field(issue.body,'Assigned role')||'Managing Editor — assign next owner'],['Checkpoint',field(issue.body,'Next checkpoint')||field(issue.body,'Target')||'See issue'],['Updated',issue.updated_at]]) {
    const p=document.createElement('p');p.className='meta';p.textContent=label+': '+value;box.append(p);
   }
   const details=document.createElement('details'),summary=document.createElement('summary'),text=document.createElement('pre');summary.textContent='Blockers, evidence and handoff history';text.textContent=issue.body||'See GitHub assignment.';details.append(summary,text);box.append(details);
   const match=(issue.body||'').match(/\/editorial\/drafts\/([a-z0-9-]+)\.md/);
   if(category(issue)==='article'&&match){
    const button=document.createElement('button'),outcome=document.createElement('p');button.type='button';button.textContent='Load shared editorial review';outcome.setAttribute('role','status');
    button.addEventListener('click',async()=>{
     button.disabled=true;outcome.textContent='Loading review…';const slug=match[1];
     try{
      const response=await fetch('https://api.github.com/repos/TheFanGuys/HVLS-360/contents/editorial/decisions/'+slug+'.json?ref=main',{cache:'no-store'});
      if(response.status===404){outcome.textContent='No shared editorial decision recorded. Publication remains unapproved.';return;}
      if(!response.ok)throw Error('HTTP '+response.status);
      const file=await response.json();const data=JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(file.content.replace(/\s/g,'')),c=>c.charCodeAt(0))));
      if(data.schema_version!==1||data.slug!==slug||data.publication_allowed!==false||!Array.isArray(data.events))throw Error('Invalid review record');
      const last=data.events[data.events.length-1];if(!last)throw Error('Empty review history');
      const current=await fetch('https://api.github.com/repos/TheFanGuys/HVLS-360/contents/editorial/drafts/'+slug+'.md?ref=main',{cache:'no-store'});
      const version=current.ok?((await current.json()).sha===last.manuscript_blob_sha?'current manuscript':'previous manuscript revision'):'current revision not checked';
      outcome.textContent=last.decision+' · '+last.recorded_at+' · '+version+' · '+last.note+' · No publication authorization';
     }catch(error){outcome.textContent='Shared review unavailable: '+error.message;}finally{button.disabled=false;}
    });box.append(button,outcome);
   }
   host.append(box);
  }
  if(!shown.length) {const p=document.createElement('p');p.className='empty';p.textContent='No matching open assignments.';host.append(p);}
 }
 async function refresh() {
  $('refresh').disabled=true;$('loadStatus').textContent='Loading shared GitHub assignments…';
  try {issues=await read();render();$('loadStatus').textContent=issues.length+' open assignments · fetched '+new Date().toLocaleString()+'. Source: GitHub Issues.';}
  catch(error) {$('loadStatus').textContent=(issues.length?'Previous results retained; refresh failed. ':'Assignments unavailable. ')+error.message;}
  finally {$('refresh').disabled=false;}
 }
 $('kind').addEventListener('change',render);$('search').addEventListener('input',render);$('refresh').addEventListener('click',refresh);refresh();
})(globalThis);
