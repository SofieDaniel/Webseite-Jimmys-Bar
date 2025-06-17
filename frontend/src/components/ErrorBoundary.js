import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log error details
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
  }

  render() {
    if (this.state.hasError) {
      // Fallback UI
      return (
        <div className="min-h-screen bg-warm-white flex items-center justify-center">
          <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8 text-center">
            <div className="text-6xl mb-4">⚠️</div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Etwas ist schief gelaufen
            </h2>
            <p className="text-gray-600 mb-6">
              Es tut uns leid, aber es ist ein unerwarteter Fehler aufgetreten. 
              Bitte laden Sie die Seite neu oder versuchen Sie es später erneut.
            </p>
            <div className="space-y-3">
              <button
                onClick={() => window.location.reload()}
                className="w-full bg-warm-brown text-white py-3 px-4 rounded-lg hover:bg-dark-brown transition-colors"
              >
                Seite neu laden
              </button>
              <button
                onClick={() => window.location.href = '/'}
                className="w-full bg-warm-beige text-dark-brown py-3 px-4 rounded-lg hover:bg-light-beige transition-colors"
              >
                Zur Startseite
              </button>
            </div>
            
            {/* Show error details in development */}
            {process.env.NODE_ENV === 'development' && (
              <details className="mt-6 text-left">
                <summary className="cursor-pointer text-sm text-gray-500 hover:text-gray-700">
                  Technische Details (nur in Entwicklung sichtbar)
                </summary>
                <div className="mt-2 p-3 bg-gray-100 rounded text-xs text-red-600 overflow-auto max-h-40">
                  <div className="font-semibold mb-2">Error:</div>
                  <div className="mb-3">{this.state.error && this.state.error.toString()}</div>
                  <div className="font-semibold mb-2">Component Stack:</div>
                  <div>{this.state.errorInfo.componentStack}</div>
                </div>
              </details>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;