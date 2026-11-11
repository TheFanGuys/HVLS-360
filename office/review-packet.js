/* Read existing public repository records only. Never writes or authorizes release. */
(function(root){
 'use strict';
 const base='https://api.github.com/repos/TheFanGuys/HVLS-360/contents/';
 async function packet(slug,transport=root.fetch){
  if(!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug))throw Error('Invalid article identifier');
  async function read(path){
   const response=await transport(base+path+'?ref=main',{cache:'no-store',headers:{Accept:'application/vnd.github+json'}});
   if(!response.ok)throw Error('HTTP '+response.status);
   const file=await response.json();return new TextDecoder().decode(Uint8Array.from(atob(file.content.replace(/\s/g,'')),c=>c.charCodeAt(0)));
  }
  const result={};
  await Promise.all([
   (async()=>{try{result.review=await read('editorial/reviews/'+slug+'-review.md');}catch(e){result.reviewError=e.message;}})(),
   (async()=>{try{
    const registry=JSON.parse(await read('office/editorial-queue.json'));const item=registry.items?.find(x=>x.slug===slug);
    if(!item)throw Error('Article missing from review registry');
    const inventory=JSON.parse(await read('editorial/media/field-photo-inventory.json'));
    const fieldAssets=(inventory.assets||[]).filter(a=>a.story===slug&&a.status!=='rejected');
    let candidates=[];
    if(item.media){
     if(!/^editorial\/media\/[a-z0-9/-]+\.json$/.test(item.media))throw Error('Invalid media registry path');
     const data=JSON.parse(await read(item.media));candidates=data.candidates||data.assets||data.images||[];
    }
    result.media=[...fieldAssets,...candidates];
   }catch(e){result.mediaError=e.message;}})()
  ]);
  return result;
 }
 root.HVLSReviewPacket={packet};
})(globalThis);
