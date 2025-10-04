import Image from "next/image"

export default function Home() {
  return (
    <div>
      Welcome to the app!!
      <input type="file" accept="image/*" />
    </div>
  );
}