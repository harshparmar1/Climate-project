import React, { useRef, useMemo, useEffect, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';
import CloudLayer from '../three/CloudLayer';
import OrbitalParticles from '../three/OrbitalParticles';
import { AtmosphereShaderMaterial } from '../three/atmosphereShader';

// 3D Star Field Particle System with Depth Movement
function StarField({ count = 1500 }) {
  const pointsRef = useRef();

  const [positions] = useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 140;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 140;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 140;
    }
    return [pos];
  }, [count]);

  useFrame((_, delta) => {
    if (pointsRef.current) {
      pointsRef.current.rotation.y += delta * 0.015;
      pointsRef.current.rotation.x += delta * 0.005;
    }
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={positions.length / 3}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.25}
        color="#67e8f9"
        transparent
        opacity={0.6}
        blending={THREE.AdditiveBlending}
        depthWrite={false}
      />
    </points>
  );
}

// Fresnel Atmospheric Scattering Rim Shader Mesh
function FresnelAtmosphere() {
  return (
    <mesh scale={[1.15, 1.15, 1.15]}>
      <sphereGeometry args={[2, 64, 64]} />
      <primitive object={AtmosphereShaderMaterial} attach="material" />
    </mesh>
  );
}

// Stylized Earth Globe with Day/Night Lighting & Specular Ocean Shading
function EarthGlobe({ mousePos }) {
  const earthGroupRef = useRef();
  const earthMeshRef = useRef();
  const targetRotation = useRef({ x: 0, y: 0 });

  // High-Tech Procedural Surface Texture
  const earthTexture = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 1024;
    canvas.height = 512;
    const ctx = canvas.getContext('2d');

    // Deep Ocean Base
    ctx.fillStyle = '#060d24';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Continent Clusters
    ctx.fillStyle = '#1e3a8a';
    for (let i = 0; i < 450; i++) {
      const x = Math.random() * canvas.width;
      const y = Math.random() * canvas.height;
      const rx = Math.random() * 90 + 20;
      const ry = Math.random() * 45 + 10;
      ctx.beginPath();
      ctx.ellipse(x, y, rx, ry, Math.random() * Math.PI, 0, Math.PI * 2);
      ctx.fill();
    }

    // Land Accents
    ctx.fillStyle = '#047857';
    for (let i = 0; i < 200; i++) {
      const x = Math.random() * canvas.width;
      const y = Math.random() * canvas.height;
      const r = Math.random() * 25 + 5;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
    }

    // Latitude & Longitude Grid Lines
    ctx.strokeStyle = 'rgba(34, 211, 238, 0.15)';
    ctx.lineWidth = 1;
    for (let y = 0; y <= canvas.height; y += 32) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(canvas.width, y);
      ctx.stroke();
    }
    for (let x = 0; x <= canvas.width; x += 64) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    }

    const texture = new THREE.CanvasTexture(canvas);
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.ClampToEdgeWrapping;
    return texture;
  }, []);

  useFrame((_, delta) => {
    if (earthGroupRef.current) {
      // Continuous slow rotation
      earthMeshRef.current.rotation.y += delta * 0.08;

      // Smooth lerp mouse parallax
      targetRotation.current.x = mousePos.current.y * 0.25;
      targetRotation.current.y = mousePos.current.x * 0.35;

      earthGroupRef.current.rotation.x += (targetRotation.current.x - earthGroupRef.current.rotation.x) * 0.05;
      earthGroupRef.current.rotation.y += (targetRotation.current.y - earthGroupRef.current.rotation.y) * 0.05;
    }
  });

  return (
    <group ref={earthGroupRef}>
      {/* Main Earth Surface Mesh */}
      <mesh ref={earthMeshRef}>
        <sphereGeometry args={[2, 64, 64]} />
        <meshStandardMaterial
          map={earthTexture}
          roughness={0.5}
          metalness={0.3}
          emissive="#0284c7"
          emissiveIntensity={0.15}
        />
      </mesh>

      {/* Cloud Layer */}
      <CloudLayer />

      {/* Fresnel Atmosphere Scattering Rim Glow */}
      <FresnelAtmosphere />

      {/* Orbital Wind Particles */}
      <OrbitalParticles count={window.innerWidth < 768 ? 100 : 250} />
    </group>
  );
}

// Multi-Stage Scroll & Camera Timeline Controller
function SceneController({ mousePos, scrollProgress }) {
  const { camera } = useThree();

  useFrame(() => {
    const progress = scrollProgress.current; // 0.0 to 1.0

    // Multi-stage scroll camera trajectory:
    // 0% -> Space (distance Z = 6.5)
    // 30% -> Approach Orbit (distance Z = 4.5)
    // 70% -> Atmosphere View (distance Z = 3.8, camera Y shift)
    // 100% -> Deep Climate Data Backdrop
    const targetZ = 6.5 - progress * 2.8;
    const targetY = progress * 0.6;
    const targetX = Math.sin(progress * Math.PI) * 0.4;

    camera.position.x += (targetX - camera.position.x) * 0.08;
    camera.position.y += (targetY - camera.position.y) * 0.08;
    camera.position.z += (targetZ - camera.position.z) * 0.08;
    camera.lookAt(0, 0, 0);
  });

  return (
    <>
      {/* Day / Night Sun Directional Light */}
      <ambientLight intensity={0.4} />
      <directionalLight position={[6, 4, 6]} intensity={1.8} color="#ffffff" />
      <directionalLight position={[-6, -4, -6]} intensity={0.25} color="#22d3ee" />

      {/* Star Field */}
      <StarField count={window.innerWidth < 768 ? 500 : 1400} />

      {/* Earth & Atmospheric Layers */}
      <EarthGlobe mousePos={mousePos} />
    </>
  );
}

export default function EarthCanvas() {
  const mousePos = useRef({ x: 0, y: 0 });
  const scrollProgress = useRef(0);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

    const handleMouseMove = (e) => {
      if (mediaQuery.matches) return;
      mousePos.current = {
        x: (e.clientX / window.innerWidth) * 2 - 1,
        y: -(e.clientY / window.innerHeight) * 2 + 1,
      };
    };

    const handleScroll = () => {
      if (mediaQuery.matches) return;
      const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (totalHeight > 0) {
        scrollProgress.current = Math.min(1, Math.max(0, window.scrollY / totalHeight));
      }
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <div className="earth-canvas-container" style={{ position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none' }}>
      <Canvas
        camera={{ position: [0, 0, 6.5], fov: 45 }}
        dpr={[1, Math.min(window.devicePixelRatio, 2)]}
        style={{ width: '100%', height: '100%' }}
      >
        <SceneController mousePos={mousePos} scrollProgress={scrollProgress} />
      </Canvas>
    </div>
  );
}
