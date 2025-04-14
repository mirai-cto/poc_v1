import { Outlet } from 'react-router-dom'
import styled from 'styled-components'
import Header from '../Header/Header'
import Footer from '../Footer/Footer'

const Main = styled.main`
  min-height: calc(100vh - 160px); // Subtract header and footer height
  padding: 2rem 0;
`

const Layout = () => {
  return (
    <>
      <Header />
      <Main>
        <div className="container">
          <Outlet />
        </div>
      </Main>
      <Footer />
    </>
  )
}

export default Layout 