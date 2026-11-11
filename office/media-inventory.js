(function(){
 'use strict';
 const $=id=>document.getElementById(id);let assets=[];
 function render(){
  const host=$('fieldInventory');host.replaceChildren();const story=$('inventoryFilter').value;
  for(const asset of assets.filter(a=>story==='all'||(story==='unassigned'?!a.story:a.story===story))){
   const card=document.createElement('article');card.className='panel';
   const heading=document.createElement('h3');heading.textContent=asset.id+' · '+asset.status;card.append(heading);
   for(const [label,value] of [['Caption proposal',asset.caption_proposal],['Identification limit',asset.identification],['Rights evidence',asset.rights_status],['Excluded',asset.exclusion_reason]]){
    if(!value)continue;const p=document.createElement('p');p.textContent=label+': '+value;card.append(p);
   }
   const p=document.createElement('p');p.textContent='Credit: '+asset.credit+' · Article release: not approved';card.append(p);host.append(card);
  }
 }
 $('inventoryFilter').addEventListener('change',render);
 (async()=>{try{
  const response=await fetch('../editorial/media/field-photo-inventory.json',{cache:'no-store'});
  if(!response.ok)throw Error('HTTP '+response.status);
  const data=await response.json();
  if(data.schema_version!==1||data.publication_allowed!==false||!Array.isArray(data.assets)||data.assets.length>200)throw Error('Invalid media inventory');
  if(data.assets.some(a=>a.publication_allowed!==false))throw Error('Inventory includes an unexpected release flag');
  assets=data.assets;render();$('inventoryStatus').textContent=assets.length+' recovered review records · '+assets.filter(a=>a.status==='retained').length+' retained derivatives · '+assets.filter(a=>a.status==='rejected').length+' excluded. Final identity, privacy and founder checks remain open.';
 }catch(error){$('inventoryStatus').textContent='Shared review unavailable: '+error.message;}})();
})();
