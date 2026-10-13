import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "The Dating Pool | UK calculator", description: "Explore the estimated share of UK adults meeting your requirements, with published data and clear source explanations." };
export default function RootLayout({ children }: Readonly<{children: React.ReactNode}>) { return <html lang="en"><body>{children}</body></html>; }
