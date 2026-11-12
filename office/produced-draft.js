/* Read-only review of an unpublished production branch; no approvals or writes. */
(function(root){
'use strict';
const repo='https://api.github.com/repos/TheFanGuys/HVLS-360',git='https://github.com/TheFanGuys/HVLS-360';
const sha40=s=>typeof s==='string'&&/^[a-f0-9]{40}$/.test(s),sha64=s=>typeof s==='string'&&/^[a-f0-9]{64}$/.test(s);
function select(queue,issue){
 if(queue.publication_allowed!==false||!Array.isArray(queue.items)||!Number.isSafeInteger(issue)||issue<1)throw Error('Invalid production queue');
 const found=queue.items.filter(x=>x.assignment_issue===issue);
 if(found.length!==1)throw Error('Draft is missing or duplicated in the queue');
 const x=found[0],branch=x.draft_branch||'production/issue-'+issue;
 if(x.publication_allowed!==false||!sha40(x.draft_head_sha)||!Number.isSafeInteger(x.draft_pr)||x.draft_pr<1||!/^[A-Za-z0-9][A-Za-z0-9/_-]{0,99}$/.test(branch))throw Error('Invalid draft delivery');
 return {...x,branch};
}
function decode(file){
 if(file.encoding!=='base64'||typeof file.content!=='string'||file.content.length>400000||!sha40(file.sha))throw Error('Invalid repository file');
 return new TextDecoder('utf-8',{fatal:true}).decode(Uint8Array.from(atob(file.content.replace(/\s/g,'')),c=>c.charCodeAt(0)));
}
async function fingerprint(text){return Array.from(new Uint8Array(await root.crypto.subtle.digest('SHA-256',new TextEncoder().encode(text))),x=>x.toString(16).padStart(2,'0')).join('');}
async function load(queue,issue,request,hash=fingerprint,parse=root.HVLSPreviewLive.parse){
 const item=select(queue,issue),branch=await request(repo+'/branches/'+item.branch);
 const revision=branch.commit?.sha;if(!sha40(revision))throw Error('Cannot establish saved branch revision');
 const base='editorial/production/issue-'+issue+'/',names=['manuscript.md','packet.json','review.md','media.json','metadata.json','sources.json'];
 const files=await Promise.all(names.map(async name=>[name,decode(await request(repo+'/contents/'+base+name+'?ref='+revision))]));
 const text=Object.fromEntries(files),draft=parse(text['manuscript.md']),packet=JSON.parse(text['packet.json']),media=JSON.parse(text['media.json']),metadata=JSON.parse(text['metadata.json']),sources=JSON.parse(text['sources.json']);
 if(packet.publication_allowed!==false||packet.assignment_issue!==issue||packet.delivery_key!=='production-issue-'+issue||media.publication_allowed!==false||metadata.publication_allowed!==false||sources.publication_allowed!==false)throw Error('Invalid unpublished package');
 const safeImage=/^editorial\/media\/(?:publisher\/[a-z0-9/-]+\.webp|original\/[a-z-]+\.svg)$/;
 if(!safeImage.test(media.file)||media.file.includes('..')||!['alt','caption','credit','rights_basis'].every(k=>typeof media[k]==='string'&&media[k].trim())||media.presentation?.lead?.fit!=='contain')throw Error('Image review record is missing or unsafe');
 const actual=await hash(text['manuscript.md']);let stale=packet.status!=='founder_review'||!sha64(packet.manuscript_sha256)||actual!==packet.manuscript_sha256||metadata.manuscript_sha256!==actual;
 for(const name of names.filter(n=>n!=='packet.json'))if(!sha64(packet.artifacts?.[name])||await hash(text[name])!==packet.artifacts[name])stale=true;
 if(!text['review.md'].includes(actual))stale=true;
 const showMedia=item.media_status!=='withheld'&&media.selection_status!=='rejected';
 return {showMedia,item,revision,draft,media,packet,manuscript_sha256:actual,stale,reviewUrl:git+'/pull/'+item.draft_pr,editUrl:git+'/edit/'+item.branch+'/'+base+'manuscript.md'};
}
async function request(url){const r=await root.fetch(url,{cache:'no-store',headers:{Accept:'application/vnd.github+json'}});if(!r.ok)throw Error('Repository read failed ('+r.status+')');return r.json();}
async function start(doc=root.document){
 const status=doc.getElementById('reviewState'),host=doc.getElementById('producedArticle');
 try{const issue=Number(new URLSearchParams(root.location.search).get('issue')),q=await request('production-queue.json'),data=await load(q,issue,request);
 doc.title=data.draft.fields.title+' | HVLS 360';doc.getElementById('draftTitle').textContent=data.draft.fields.title;doc.getElementById('draftCategory').textContent=data.draft.fields.category;
 host.innerHTML=root.HVLSPreviewLive.render(data.draft.body);
 if(data.showMedia){const img=doc.getElementById('draftImage');img.src='../'+data.media.file;img.alt=data.media.alt;doc.getElementById('imageCaption').textContent=data.media.caption+' — '+data.media.credit;doc.getElementById('draftMedia').hidden=false;}else{doc.getElementById('draftImage').removeAttribute('src');doc.getElementById('draftMedia').hidden=true;}
 doc.getElementById('editDraft').href=data.editUrl;doc.getElementById('reviewPackage').href=data.reviewUrl;doc.getElementById('draftActions').hidden=false;
 status.textContent='Saved draft · '+data.revision.slice(0,7)+' · '+(!data.showMedia?'Image withheld; suitable replacement pending.':data.stale?'Text or supporting records changed. Earlier reviews need refreshing.':'Recorded reviews match this saved text.');status.dataset.stale=String(data.stale);
 }catch(e){host.replaceChildren();doc.getElementById('draftMedia').hidden=true;doc.getElementById('draftActions').hidden=true;status.dataset.error='true';status.textContent='This saved draft could not load. Return to Produced Drafts and open its review package to read or edit it.';}
}
root.HVLSProducedDraft={select,decode,load,start};if(root.document)start();
})(globalThis);
