import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function HomepageFeatures() {
  const {siteConfig} = useDocusaurusContext();
  const features = siteConfig.customFields?.features || [];

  if (features.length === 0) {
    return null;
  }

  return (
    <section style={{padding: '60px 0'}}>
      <div className="container">
        <div className="row" style={{justifyContent: 'center'}}>
          {features.map((feature, idx) => (
            <div className="col col--4" key={idx} style={{padding: '20px'}}>
              <div className="card" style={{
                height: '100%',
                padding: '20px',
                textAlign: 'center',
                borderRadius: '8px',
                boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
              }}>
                <div style={{
                  fontSize: '3rem',
                  marginBottom: '15px'
                }}>
                  {feature.icon}
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}