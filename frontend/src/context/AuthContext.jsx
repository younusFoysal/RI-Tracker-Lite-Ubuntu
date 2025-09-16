import React, { createContext, useState, useContext, useEffect } from 'react';
import {toast} from "sonner";

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(null);
    const [token, setToken] = useState(null);
    const [loading, setLoading] = useState(true); // When pywebview is ready AND auth check is done
    const [pywebviewReady, setPywebviewReady] = useState(false); // Only pywebview

    // Listen for pywebview readiness
    useEffect(() => {
        const handleReady = () => setPywebviewReady(true);

        const checkPywebviewReady = () => {
            // Check if both pywebview object and its API are available
            return window.pywebview && 
                   window.pywebview.api && 
                   typeof window.pywebview.api.is_authenticated === 'function';
        };

        if (checkPywebviewReady()) {
            setPywebviewReady(true);
        } else {
            window.addEventListener('pywebviewready', handleReady);
            
            // Also check periodically in case the event doesn't fire
            const checkInterval = setInterval(() => {
                if (checkPywebviewReady()) {
                    setPywebviewReady(true);
                    clearInterval(checkInterval);
                }
            }, 100);
            
            // Clean up interval after 10 seconds to avoid infinite checking
            setTimeout(() => clearInterval(checkInterval), 10000);
        }

        return () => {
            window.removeEventListener('pywebviewready', handleReady);
        };
    }, []);

    // When pywebview is ready, check authentication
    useEffect(() => {
        const checkAuthStatus = async () => {
            try {
                // Additional safety check to ensure the API methods exist
                if (!window.pywebview?.api?.is_authenticated || !window.pywebview?.api?.get_current_user) {
                    console.log('Auth API methods not yet available, retrying...');
                    // Retry after a short delay
                    setTimeout(checkAuthStatus, 500);
                    return;
                }

                const isAuthResponse = await window.pywebview.api.is_authenticated();
                console.log('Auth check response:', isAuthResponse);
                
                if (isAuthResponse && isAuthResponse.authenticated) {
                    const userResponse = await window.pywebview.api.get_current_user();
                    console.log('User data response:', userResponse);
                    
                    if (userResponse && userResponse.success && userResponse.user) {
                        setCurrentUser(userResponse.user);
                        setToken("token-exists");
                        console.log('Authentication restored from stored data');
                    }
                }
            } catch (error) {
                console.error('Auth check error:', error);
                // If the auth check fails, try one more time after a delay
                setTimeout(async () => {
                    try {
                        if (window.pywebview?.api?.is_authenticated) {
                            const retryResponse = await window.pywebview.api.is_authenticated();
                            if (retryResponse && retryResponse.authenticated) {
                                const userResponse = await window.pywebview.api.get_current_user();
                                if (userResponse && userResponse.success && userResponse.user) {
                                    setCurrentUser(userResponse.user);
                                    setToken("token-exists");
                                    console.log('Authentication restored on retry');
                                }
                            }
                        }
                    } catch (retryError) {
                        console.error('Auth retry failed:', retryError);
                    } finally {
                        setLoading(false);
                    }
                }, 1000);
                return;
            } finally {
                // Only set loading to false if we're not retrying
                if (window.pywebview?.api?.is_authenticated) {
                    setLoading(false);
                }
            }
        };

        if (pywebviewReady) {
            checkAuthStatus();
        }
    }, [pywebviewReady]);

    const login = async (email, password, rememberMe = false) => {
        try {
            const response = await window.pywebview.api.login(email, password, rememberMe);
            if (response.success) {
                setCurrentUser(response.data.employee);
                setToken("token-exists");
                return { success: true };
            } else {
                return { success: false, message: response.message || 'Login failed' };
            }
        } catch (error) {
            console.error('Login error:', error);
            return { success: false, message: 'An error occurred during login' };
        }
    };

    const logout = async () => {
        try {
            await window.pywebview.api.logout();
            setToken(null);
            setCurrentUser(null);
            toast.success("Logged out successfully!");
        } catch (error) {
            console.error('Logout error:', error);
        }
    };

    const isAuthenticated = () => !!token;

    const getProfile = async () => {
        try {
            if (!isAuthenticated()) return { success: false, message: 'Not authenticated' };
            return await window.pywebview.api.get_profile();
        } catch (error) {
            console.error('Profile error:', error);
            return { success: false, message: 'An error occurred while fetching profile' };
        }
    };

    const value = {
        currentUser,
        token,
        login,
        logout,
        isAuthenticated,
        getProfile,
        loading,
    };

    return (
        <AuthContext.Provider value={value}>
            {loading ? (
                <div className="w-full h-screen flex items-center justify-center bg-white dark:bg-gray-900">
                    <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-500"></div>
                </div>
            ) : (
                children
            )}
        </AuthContext.Provider>
    );
};
