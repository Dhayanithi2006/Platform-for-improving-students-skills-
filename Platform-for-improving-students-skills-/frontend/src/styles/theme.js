// Dynamic theme configuration
export const theme = {
  colors: {
    light: {
      bg: {
        primary: '#ffffff',
        secondary: '#f8fafc',
        card: '#ffffff',
      },
      text: {
        primary: '#1e293b',
        secondary: '#64748b',
      },
      border: '#e2e8f0',
    },
    dark: {
      bg: {
        primary: '#0f172a',
        secondary: '#1e293b',
        card: '#334155',
      },
      text: {
        primary: '#f1f5f9',
        secondary: '#cbd5e1',
      },
      border: '#475569',
    },
  },
  
  getThemeColors: (isDark) => isDark ? theme.colors.dark : theme.colors.light,
  
  gradients: {
    primary: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    success: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    warning: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
    danger: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
  },
  
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  },
};

// Dynamic risk colors
export const getRiskColor = (riskLevel) => {
  switch(riskLevel?.toLowerCase()) {
    case 'high': return '#ef4444';
    case 'medium': return '#f59e0b';
    case 'low': return '#10b981';
    default: return '#6b7280';
  }
};

// Dynamic mastery color
export const getMasteryColor = (mastery) => {
  if (mastery >= 80) return '#10b981';
  if (mastery >= 60) return '#f59e0b';
  return '#ef4444';
};

// Animation presets
export const animations = {
  fadeIn: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    transition: { duration: 0.3 }
  },
  slideUp: {
    initial: { y: 20, opacity: 0 },
    animate: { y: 0, opacity: 1 },
    transition: { duration: 0.4 }
  },
  scaleIn: {
    initial: { scale: 0.9, opacity: 0 },
    animate: { scale: 1, opacity: 1 },
    transition: { duration: 0.3 }
  }
};