export default function showToast(message, type = 'success', duration = 3500){
  try{
    const id = 'sp-toast-root'
    let root = document.getElementById(id)
    if(!root){
      root = document.createElement('div')
      root.id = id
      root.style.position = 'fixed'
      root.style.right = '18px'
      root.style.bottom = '18px'
      root.style.zIndex = 99999
      root.style.display = 'flex'
      root.style.flexDirection = 'column'
      root.style.gap = '8px'
      document.body.appendChild(root)
    }
    const el = document.createElement('div')
    el.className = `sp-toast sp-toast-${type}`
    el.textContent = message
    el.style.minWidth = '160px'
    el.style.padding = '10px 14px'
    el.style.borderRadius = '10px'
    el.style.color = '#0b1220'
    el.style.fontWeight = '600'
    el.style.boxShadow = '0 8px 30px rgba(2,6,23,0.6)'
    el.style.opacity = '0'
    el.style.transform = 'translateY(8px)'
    el.style.transition = 'all .28s cubic-bezier(.2,.9,.2,1)'
    if(type === 'error') el.style.background = '#fecaca'
    else el.style.background = '#bbf7d0'
    root.appendChild(el)
    // enter
    requestAnimationFrame(()=>{
      el.style.opacity = '1'
      el.style.transform = 'translateY(0)'
    })
    setTimeout(()=>{
      // exit
      el.style.opacity = '0'
      el.style.transform = 'translateY(8px)'
      setTimeout(()=>{ try{ root.removeChild(el) }catch(e){} }, 300)
    }, duration)
  }catch(e){ console.warn('Toast error', e) }
}
