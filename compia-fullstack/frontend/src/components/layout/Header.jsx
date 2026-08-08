import {useState} from 'react';
import {Link,NavLink} from 'react-router-dom';
import {useAuth} from '../../hooks/useAuth';
import {useCart} from '../../hooks/useCart';
export function Header(){
  const{user,logout}=useAuth(),{count}=useCart(),[open,setOpen]=useState(false),admin=user&&['admin','editor','seller'].includes(user.role);
  const close=()=>setOpen(false);
  return <><div className="topbar">Tecnologia que vira conhecimento • COMPIA Editora</div><header className="header"><div className="container nav"><Link className="logo" to="/" onClick={close}><span className="logo-mark">C</span><span>COMPIA</span></Link><button className="menu-btn" aria-label="Abrir menu" onClick={()=>setOpen(v=>!v)}>☰</button><nav className={`nav-links ${open?'open':''}`}><NavLink to="/" end onClick={close}>Início</NavLink><NavLink to="/produtos" onClick={close}>Catálogo</NavLink>{user?<NavLink to="/conta" onClick={close}>Minha conta</NavLink>:<NavLink to="/login" onClick={close}>Entrar</NavLink>}{admin&&<NavLink to="/admin" onClick={close}>Admin</NavLink>}{user&&<button className="link-button" onClick={()=>{logout();close()}}>Sair</button>}<NavLink className="cart-link" to="/carrinho" onClick={close}>Carrinho <span className="cart-badge">{count}</span></NavLink></nav></div></header></>
}
