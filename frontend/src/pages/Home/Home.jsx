import { Link } from 'react-router-dom'
import styled from 'styled-components'

const Hero = styled.section`
  text-align: center;
  padding: 4rem 0;
`

const HeroTitle = styled.h1`
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  color: var(--secondary-color);
`

const HeroSubtitle = styled.p`
  font-size: 1.25rem;
  color: var(--dark-gray);
  margin-bottom: 2rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
`

const CTAButton = styled(Link)`
  padding: 0.75rem 2rem;
  font-size: 1.125rem;
  font-weight: 600;
`

const FeaturesSection = styled.section`
  padding: 4rem 0;
  background-color: white;
`

const FeaturesTitle = styled.h2`
  text-align: center;
  margin-bottom: 3rem;
  color: var(--secondary-color);
`

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
`

const FeatureCard = styled.div`
  background-color: var(--background-color);
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
`

const FeatureIcon = styled.div`
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
`

const FeatureTitle = styled.h3`
  margin-bottom: 1rem;
  color: var(--secondary-color);
`

const FeatureDescription = styled.p`
  color: var(--dark-gray);
`

const Home = () => {
  return (
    <>
      <Hero>
        <HeroTitle>CNC Tool Recommender</HeroTitle>
        <HeroSubtitle>
          Optimize your machining operations with intelligent tool recommendations
          and speed & feed calculations based on your CAD files and machine capabilities.
        </HeroSubtitle>
        <CTAButton to="/upload" className="btn">
          Upload CAD File
        </CTAButton>
      </Hero>

      <FeaturesSection>
        <div className="container">
          <FeaturesTitle>Key Features</FeaturesTitle>
          <FeaturesGrid>
            <FeatureCard>
              <FeatureIcon>📊</FeatureIcon>
              <FeatureTitle>Intelligent Tool Selection</FeatureTitle>
              <FeatureDescription>
                Get personalized tool recommendations based on your CAD geometry and machine specifications.
              </FeatureDescription>
            </FeatureCard>

            <FeatureCard>
              <FeatureIcon>⚙️</FeatureIcon>
              <FeatureTitle>Optimized Speed & Feed</FeatureTitle>
              <FeatureDescription>
                Calculate optimal cutting parameters adjusted for tool wear and material properties.
              </FeatureDescription>
            </FeatureCard>

            <FeatureCard>
              <FeatureIcon>📈</FeatureIcon>
              <FeatureTitle>Continuous Improvement</FeatureTitle>
              <FeatureDescription>
                Provide feedback after machining to improve future recommendations.
              </FeatureDescription>
            </FeatureCard>
          </FeaturesGrid>
        </div>
      </FeaturesSection>
    </>
  )
}

export default Home 