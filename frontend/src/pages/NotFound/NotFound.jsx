import { Link } from 'react-router-dom'
import styled from 'styled-components'

const NotFoundContainer = styled.div`
  text-align: center;
  padding: 5rem 0;
`

const NotFoundTitle = styled.h1`
  font-size: 4rem;
  color: var(--secondary-color);
  margin-bottom: 1rem;
`

const NotFoundText = styled.p`
  font-size: 1.25rem;
  color: var(--dark-gray);
  margin-bottom: 2rem;
`

const HomeButton = styled(Link)`
  display: inline-block;
`

const NotFound = () => {
  return (
    <NotFoundContainer>
      <NotFoundTitle>404</NotFoundTitle>
      <NotFoundText>Oops! The page you are looking for doesn't exist.</NotFoundText>
      <HomeButton to="/" className="btn">
        Go to Home
      </HomeButton>
    </NotFoundContainer>
  )
}

export default NotFound 