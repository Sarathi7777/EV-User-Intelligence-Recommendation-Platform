import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import envConfig from "../env.config";

const Register = ({ onLogin }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
    vehicleType: "",
    agreeToTerms: false
  });
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({});

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ""
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.firstName.trim()) {
      newErrors.firstName = "First name is required";
    }

    if (!formData.lastName.trim()) {
      newErrors.lastName = "Last name is required";
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Please enter a valid email";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
    }

    if (!formData.vehicleType) {
      newErrors.vehicleType = "Please select your vehicle type";
    }

    if (formData.phone && !/^\+?[0-9\-()\s]{7,20}$/.test(formData.phone)) {
      newErrors.phone = "Please enter a valid phone number";
    }

    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = "You must agree to the terms and conditions";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    
    try {
      // Call the real registration endpoint
      const response = await fetch(`${envConfig.BACKEND_API_URL}/login/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          confirm_password: formData.confirmPassword,
          first_name: formData.firstName,
          last_name: formData.lastName,
          vehicle_type: formData.vehicleType,
          phone: formData.phone
        }),
      });

      if (!response.ok) {
        let message = 'Registration failed';
        try {
          const ct = response.headers.get('content-type') || '';
          if (ct.includes('application/json')) {
            const errorData = await response.json();
            message = errorData.detail || message;
          } else {
            message = (await response.text()) || message;
          }
        } catch {}
        throw new Error(message);
      }

      const userData = await response.json();
      // Attach first/last name for UI if backend doesn't return them
      userData.first_name = userData.first_name || formData.firstName;
      userData.last_name = userData.last_name || formData.lastName;
      userData.phone = userData.phone || formData.phone;
      
      // Auto-login the user
      onLogin(userData);
      navigate('/home');
    } catch (error) {
      console.error('Registration error:', error);
      const message = (error && error.message) ? error.message : 'Registration failed. Please try again.';
      alert(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px',
      fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif'
    }}>
      {/* Animated Background Elements */}
      <div style={{
        position: 'absolute',
        top: '5%',
        left: '5%',
        width: '150px',
        height: '150px',
        background: 'rgba(255, 255, 255, 0.1)',
        borderRadius: '50%',
        animation: 'float 7s ease-in-out infinite'
      }}></div>
      <div style={{
        position: 'absolute',
        bottom: '5%',
        right: '5%',
        width: '200px',
        height: '200px',
        background: 'rgba(255, 255, 255, 0.1)',
        borderRadius: '50%',
        animation: 'float 9s ease-in-out infinite reverse'
      }}></div>
      <div style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '100px',
        height: '100px',
        background: 'rgba(255, 255, 255, 0.05)',
        borderRadius: '50%',
        animation: 'float 5s ease-in-out infinite'
      }}></div>

      {/* Main Register Card */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        borderRadius: '20px',
        padding: '40px',
        boxShadow: '0 20px 40px rgba(0, 0, 0, 0.1)',
        width: '100%',
        maxWidth: '500px',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {/* EV User Intelligence Logo */}
        <div style={{
          textAlign: 'center',
          marginBottom: '30px'
        }}>
          <div style={{
            width: '60px',
            height: '60px',
            background: 'linear-gradient(135deg, #28a745, #20c997)',
            borderRadius: '15px',
            margin: '0 auto 15px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '24px',
            color: 'white',
            fontWeight: 'bold'
          }}>
            ⚡
          </div>
          <h1 style={{
            margin: '0',
            fontSize: '28px',
            fontWeight: '700',
            color: '#2d3748',
            marginBottom: '5px'
          }}>
            Join EV User Intelligence
          </h1>
          <p style={{
            margin: '0',
            color: '#718096',
            fontSize: '14px'
          }}>
            Create your account and start your eco-friendly journey
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          {/* Name Fields */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '15px',
            marginBottom: '20px'
          }}>
            <div>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '14px',
                fontWeight: '500',
                color: '#4a5568'
              }}>
                First Name *
              </label>
              <input
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleInputChange}
                placeholder="Peiii"
                required
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: `2px solid ${errors.firstName ? '#e53e3e' : '#e2e8f0'}`,
                  borderRadius: '10px',
                  fontSize: '16px',
                  transition: 'all 0.3s ease',
                  outline: 'none',
                  boxSizing: 'border-box'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#28a745';
                  e.target.style.boxShadow = '0 0 0 3px rgba(40, 167, 69, 0.1)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = errors.firstName ? '#e53e3e' : '#e2e8f0';
                  e.target.style.boxShadow = 'none';
                }}
              />
              {errors.firstName && (
                <p style={{
                  margin: '5px 0 0 0',
                  fontSize: '12px',
                  color: '#e53e3e'
                }}>
                  {errors.firstName}
                </p>
              )}
            </div>

            <div>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '14px',
                fontWeight: '500',
                color: '#4a5568'
              }}>
                Last Name *
              </label>
              <input
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleInputChange}
                placeholder="Doe"
                required
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: `2px solid ${errors.lastName ? '#e53e3e' : '#e2e8f0'}`,
                  borderRadius: '10px',
                  fontSize: '16px',
                  transition: 'all 0.3s ease',
                  outline: 'none',
                  boxSizing: 'border-box'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#28a745';
                  e.target.style.boxShadow = '0 0 0 3px rgba(40, 167, 69, 0.1)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = errors.lastName ? '#e53e3e' : '#e2e8f0';
                  e.target.style.boxShadow = 'none';
                }}
              />
              {errors.lastName && (
                <p style={{
                  margin: '5px 0 0 0',
                  fontSize: '12px',
                  color: '#e53e3e'
                }}>
                  {errors.lastName}
                </p>
              )}
            </div>
          </div>

          {/* Email Field */}
          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              marginBottom: '8px',
              fontSize: '14px',
              fontWeight: '500',
              color: '#4a5568'
            }}>
              Email Address *
            </label>
            <div style={{
              position: 'relative',
              display: 'flex',
              alignItems: 'center'
            }}>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="peiiiminion@gmail.com"
                required
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: `2px solid ${errors.email ? '#e53e3e' : '#e2e8f0'}`,
                  borderRadius: '10px',
                  fontSize: '16px',
                  transition: 'all 0.3s ease',
                  outline: 'none',
                  boxSizing: 'border-box'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#28a745';
                  e.target.style.boxShadow = '0 0 0 3px rgba(40, 167, 69, 0.1)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = errors.email ? '#e53e3e' : '#e2e8f0';
                  e.target.style.boxShadow = 'none';
                }}
              />
              <span style={{
                position: 'absolute',
                right: '12px',
                color: '#a0aec0',
                fontSize: '18px'
              }}>
                📧
              </span>
            </div>
            {errors.email && (
              <p style={{
                margin: '5px 0 0 0',
                fontSize: '12px',
                color: '#e53e3e'
              }}>
                {errors.email}
              </p>
            )}
          </div>

          {/* Mobile Number */}
          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              marginBottom: '8px',
              fontSize: '14px',
              fontWeight: '500',
              color: '#4a5568'
            }}>
              Mobile Number (optional)
            </label>
            <div style={{
              position: 'relative',
              display: 'flex',
              alignItems: 'center'
            }}>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleInputChange}
                placeholder="+1 (555) 123-4567"
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: `2px solid ${errors.phone ? '#e53e3e' : '#e2e8f0'}`,
                  borderRadius: '10px',
                  fontSize: '16px',
                  transition: 'all 0.3s ease',
                  outline: 'none',
                  boxSizing: 'border-box'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#28a745';
                  e.target.style.boxShadow = '0 0 0 3px rgba(40, 167, 69, 0.1)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = errors.phone ? '#e53e3e' : '#e2e8f0';
                  e.target.style.boxShadow = 'none';
                }}
              />
              <span style={{
                position: 'absolute',
                right: '12px',
                color: '#a0aec0',
                fontSize: '18px'
              }}>
                📱
              </span>
            </div>
            {errors.phone && (
              <p style={{
                margin: '5px 0 0 0',
                fontSize: '12px',
                color: '#e53e3e'
              }}>
                {errors.phone}
              </p>
            )}
          </div>

          {/* Vehicle Type */}
          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              marginBottom: '8px',
              fontSize: '14px',
              fontWeight: '500',
              color: '#4a5568'
            }}>
              Vehicle Type *
            </label>
            <select
              name="vehicleType"
              value={formData.vehicleType}
              onChange={handleInputChange}
              required
              style={{
                width: '100%',
                padding: '12px 16px',
                border: `2px solid ${errors.vehicleType ? '#e53e3e' : '#e2e8f0'}`,
                borderRadius: '10px',
                fontSize: '16px',
                transition: 'all 0.3s ease',
                outline: 'none',
                boxSizing: 'border-box',
                background: 'white'
              }}
              onFocus={(e) => {
                e.target.style.borderColor = '#28a745';
                e.target.style.boxShadow = '0 0 0 3px rgba(40, 167, 69, 0.1)';
              }}
              onBlur={(e) => {
                e.target.style.borderColor = errors.vehicleType ? '#e53e3e' : '#e2e8f0';
                e.target.style.boxShadow = 'none';
              }}
            >
              <option value="">Select your vehicle type</option>
              <option value="tesla">Tesla</option>
              <option value="nissan">Nissan Leaf</option>
              <option value="chevrolet">Chevrolet Bolt</option>
              <option value="bmw">BMW i3</option>
              <option value="audi">Audi e-tron</option>
              <option value="mercedes">Mercedes EQC</option>
              <option value="hyundai">Hyundai Kona Electric</option>
              <option value="kia">Kia Niro EV</option>
              <option value="ford">Ford Mustang Mach-E</option>
              <option value="other">Other</option>
            </select>
            {errors.vehicleType && (
              <p style={{
                margin: '5px 0 0 0',
                fontSize: '12px',
                color: '#e53e3e'
              }}>
                {errors.vehicleType}
              </p>
            )}
          </div>

          {/* Password Fields */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '15px',
            marginBottom: '20px'
          }}>
            <div>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '14px',
                fontWeight: '500',
                color: '#4a5568'
              }}>
                Password *
              </label>
              <div style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center'
              }}>
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="Min 6 characters"
                  required
                  style={{
                    width: '100%',
                    padding: '12px 16px',
                    paddingRight: '50px',
                    border: `2px solid ${errors.password ? '#e53e3e' : '#e2e8f0'}`,
                    borderRadius: '10px',
                    fontSize: '16px',
                    transition: 'all 0.3s ease',
                    outline: 'none',
                    boxSizing: 'border-box'
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = '#28a745';
                    e.target.style.boxShadow = '0 0 0 3px rgba(40, 167, 69, 0.1)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = errors.password ? '#e53e3e' : '#e2e8f0';
                    e.target.style.boxShadow = 'none';
                  }}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    position: 'absolute',
                    right: '12px',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    fontSize: '16px',
                    color: '#a0aec0'
                  }}
                >
                  {showPassword ? '🙈' : '👁️'}
                </button>
              </div>
              {errors.password && (
                <p style={{
                  margin: '5px 0 0 0',
                  fontSize: '12px',
                  color: '#e53e3e'
                }}>
                  {errors.password}
                </p>
              )}
            </div>

            <div>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '14px',
                fontWeight: '500',
                color: '#4a5568'
              }}>
                Confirm Password *
              </label>
              <div style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center'
              }}>
                <input
                  type={showConfirmPassword ? "text" : "password"}
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  placeholder="Confirm password"
                  required
                  style={{
                    width: '100%',
                    padding: '12px 16px',
                    paddingRight: '50px',
                    border: `2px solid ${errors.confirmPassword ? '#e53e3e' : '#e2e8f0'}`,
                    borderRadius: '10px',
                    fontSize: '16px',
                    transition: 'all 0.3s ease',
                    outline: 'none',
                    boxSizing: 'border-box'
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = '#28a745';
                    e.target.style.boxShadow = '0 0 0 3px rgba(40, 167, 69, 0.1)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = errors.confirmPassword ? '#e53e3e' : '#e2e8f0';
                    e.target.style.boxShadow = 'none';
                  }}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  style={{
                    position: 'absolute',
                    right: '12px',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    fontSize: '16px',
                    color: '#a0aec0'
                  }}
                >
                  {showConfirmPassword ? '🙈' : '👁️'}
                </button>
              </div>
              {errors.confirmPassword && (
                <p style={{
                  margin: '5px 0 0 0',
                  fontSize: '12px',
                  color: '#e53e3e'
                }}>
                  {errors.confirmPassword}
                </p>
              )}
            </div>
          </div>

          {/* Terms and Conditions */}
          <div style={{ marginBottom: '25px' }}>
            <label style={{
              display: 'flex',
              alignItems: 'flex-start',
              fontSize: '14px',
              color: '#4a5568',
              cursor: 'pointer',
              lineHeight: '1.5'
            }}>
              <input
                type="checkbox"
                name="agreeToTerms"
                checked={formData.agreeToTerms}
                onChange={handleInputChange}
                style={{
                  marginRight: '10px',
                  marginTop: '2px',
                  transform: 'scale(1.2)'
                }}
              />
              <span>
                I agree to the{' '}
                <Link to="/terms" style={{
                  color: '#28a745',
                  textDecoration: 'none',
                  fontWeight: '500'
                }}>
                  Terms of Service
                </Link>
                {' '}and{' '}
                <Link to="/privacy" style={{
                  color: '#28a745',
                  textDecoration: 'none',
                  fontWeight: '500'
                }}>
                  Privacy Policy
                </Link>
                *
              </span>
            </label>
            {errors.agreeToTerms && (
              <p style={{
                margin: '5px 0 0 0',
                fontSize: '12px',
                color: '#e53e3e'
              }}>
                {errors.agreeToTerms}
              </p>
            )}
          </div>

          {/* Register Button */}
          <button
            type="submit"
            disabled={isLoading}
            style={{
              width: '100%',
              padding: '14px',
              background: isLoading ? '#a0aec0' : 'linear-gradient(135deg, #28a745, #20c997)',
              color: 'white',
              border: 'none',
              borderRadius: '10px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s ease',
              position: 'relative',
              overflow: 'hidden'
            }}
            onMouseEnter={(e) => {
              if (!isLoading) {
                e.target.style.transform = 'translateY(-2px)';
                e.target.style.boxShadow = '0 10px 20px rgba(40, 167, 69, 0.3)';
              }
            }}
            onMouseLeave={(e) => {
              if (!isLoading) {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = 'none';
              }
            }}
          >
            {isLoading ? (
              <span>Creating account... ⚡</span>
            ) : (
              <span>Create Account ⚡</span>
            )}
          </button>
        </form>

        {/* Login Link */}
        <div style={{
          textAlign: 'center',
          marginTop: '25px',
          fontSize: '14px',
          color: '#4a5568'
        }}>
          Already have an account?{' '}
          <Link to="/login" style={{
            color: '#28a745',
            textDecoration: 'none',
            fontWeight: '600'
          }}>
            Sign in here
          </Link>
        </div>

        {/* Benefits Section */}
        <div style={{
          marginTop: '25px',
          padding: '20px',
          background: 'rgba(40, 167, 69, 0.05)',
          borderRadius: '15px',
          border: '1px solid rgba(40, 167, 69, 0.1)'
        }}>
          <h4 style={{
            margin: '0 0 15px 0',
            fontSize: '16px',
            fontWeight: '600',
            color: '#28a745'
          }}>
            🌱 Join the Green Revolution
          </h4>
          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '10px',
            fontSize: '12px',
            color: '#4a5568'
          }}>
            <div>⚡ Smart Charging</div>
            <div>🌍 Eco Tracking</div>
            <div>🎯 AI Recommendations</div>
            <div>📊 Analytics Dashboard</div>
          </div>
        </div>
      </div>

      {/* CSS Animations */}
      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }
      `}</style>
    </div>
  );
};

export default Register; 