import * as THREE from 'three';

// Custom GLSL Fresnel Atmospheric Scattering Shader
export const AtmosphereShaderMaterial = new THREE.ShaderMaterial({
  vertexShader: `
    varying vec3 vNormal;
    varying vec3 vPosition;
    void main() {
      vNormal = normalize(normalMatrix * normal);
      vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    varying vec3 vNormal;
    varying vec3 vPosition;
    uniform vec3 color;
    void main() {
      vec3 viewVector = normalize(-vPosition);
      float intensity = pow(0.7 - dot(vNormal, viewVector), 2.5);
      gl_FragColor = vec4(color, 1.0) * intensity * 1.5;
    }
  `,
  uniforms: {
    color: { value: new THREE.Color('#22d3ee') },
  },
  blending: THREE.AdditiveBlending,
  side: THREE.BackSide,
  transparent: true,
  depthWrite: false,
});
