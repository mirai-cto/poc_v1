import { Link, NavLink } from 'react-router-dom'
import styled from 'styled-components'

const HeaderContainer = styled.header`
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
`

const HeaderContent = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`

const Logo = styled(Link)`
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color);
  text-decoration: none;

  &:hover {
    text-decoration: none;
  }
`

const Nav = styled.nav`
  display: flex;
  gap: 1.5rem;
`

const NavItem = styled(NavLink)`
  color: var(--text-color);
  text-decoration: none;
  font-weight: 500;
  position: relative;

  &:hover {
    color: var(--primary-color);
    text-decoration: none;
  }

  &.active {
    color: var(--primary-color);

    &::after {
      content: '';
      position: absolute;
      bottom: -4px;
      left: 0;
      width: 100%;
      height: 2px;
      background-color: var(--primary-color);
    }
  }
`

const Header = () => {
  return (
    <HeaderContainer>
      <div className="container">
        <HeaderContent>
          <Logo to="/">CNC Tool Recommender</Logo>
          <Nav>
            <NavItem to="/" end>Home</NavItem>
            <NavItem to="/upload">Upload CAD</NavItem>
          </Nav>
        </HeaderContent>
      </div>
    </HeaderContainer>
  )
}

export default Header 