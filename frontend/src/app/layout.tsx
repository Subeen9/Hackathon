import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import ThemeRegistry from "../../src/app/components/ThemeRegistry";
import Navbar from "../../src/app/components/Navbar";
import Footer from "../../src/app/components/Footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Texti-Fy",
  description: "Digitizing and translating manuscripts",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable}`}
        style={{
          minHeight: "100vh",
          margin: 0,
          padding: 0,
          display: "flex",
          flexDirection: "column",
          backgroundColor: "#fefcf9", // matches manuscript tone
        }}
      >
        <ThemeRegistry>
          <Navbar />
          <main
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              overflowX: "hidden",
              overflowY: "auto",
              paddingBottom: "1rem", // space above footer
            }}
          >
            {children}
          </main>
          <Footer />
        </ThemeRegistry>
      </body>
    </html>
  );
}
