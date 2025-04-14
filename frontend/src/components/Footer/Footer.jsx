import styled from 'styled-components'

const FooterContainer = styled.footer`
  background-color: var(--secondary-color);
  color: white;
  padding: 2rem 0;
`

const FooterContent = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
`

const Copyright = styled.p`
  margin: 0;
`

const FooterLinks = styled.div`
  display: flex;
  gap: 1.5rem;
`

const FooterLink = styled.a`
  color: white;
  opacity: 0.8;
  transition: opacity 0.2s;
  
  &:hover {
    opacity: 1;
    text-decoration: none;
  }
`

const Footer = () => {
  const year = new Date().getFullYear()
  
  return (
    <FooterContainer>
      <div className="container">
        <FooterContent>
          <Copyright>
            &copy; {year} CNC Tool Recommender. All rights reserved.
          </Copyright>
          <FooterLinks>
            <FooterLink href="#">Privacy Policy</FooterLink>
            <FooterLink href="#">Terms of Service</FooterLink>
            <FooterLink href="#">Contact</FooterLink>
          </FooterLinks>
        </FooterContent>
      </div>
    </FooterContainer>
  )
}

export default Footer 