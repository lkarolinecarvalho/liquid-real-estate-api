export default function Header() {
  return (
    <header className="border-b border-liquid-gray-800 bg-liquid-black/80 backdrop-blur-md sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-orange rounded-lg flex items-center justify-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="w-6 h-6 text-white"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"
                />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold">
                <span className="text-white">Liquid</span>
                <span className="text-liquid-orange">.</span>
              </h1>
              <p className="text-xs text-liquid-gray-400">Simulador de Financiamento</p>
            </div>
          </div>

          {/* Info */}
          <div className="hidden md:flex items-center space-x-4">
            <div className="px-4 py-2 bg-liquid-gray-900 rounded-lg border border-liquid-gray-700">
              <p className="text-xs text-liquid-gray-400">Powered by</p>
              <p className="text-sm font-semibold text-liquid-orange">#BeLiquid</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}