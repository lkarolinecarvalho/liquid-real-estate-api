import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Simulador de Financiamento Imobiliário | Liquid",
  description: "Simule seu financiamento imobiliário com taxas reais e indicadores econômicos atualizados.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <div className="min-h-screen bg-liquid-black">
          {children}
        </div>
      </body>
    </html>
  );
}