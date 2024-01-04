import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function fromBytesInt64(bytes: Uint8Array): bigint {
  const { buffer } = new Uint8Array(bytes);
  const dataview = new DataView(buffer);
  return dataview.getBigInt64(0);
}

function toBytesInt64(num: bigint) {
  const arr = new ArrayBuffer(8);
  const view = new DataView(arr);
  view.setBigInt64(0, num, false); // byteOffset = 0; litteEndian = false
  return new Uint8Array(arr);
}

function fromBytesInt16(bytes: Uint8Array): number {
  const { buffer } = new Uint8Array(bytes);
  const dataview = new DataView(buffer);
  return dataview.getInt16(0);
}

function toBytesInt16(num: number) {
  const arr = new ArrayBuffer(2);
  const view = new DataView(arr);
  view.setInt16(0, num, false); // byteOffset = 0; litteEndian = false
  return new Uint8Array(arr);
}

function App() {
  const [device, setDevie] = useState<HIDDevice>();

  const connect = async () => {
    const device = await navigator.hid.requestDevice({ filters: [] });
    device[0].open();
    setDevie(device[0]);
    console.log("device: ", device[0]);
  };

  const send = async () => {
    const enc = new TextEncoder();
    const data = enc.encode(
      "123456789012345678901234567890123456789012345678901234567890123",
    );
    console.log("data: ", data);
    device?.sendReport(0x08, data);
  };

  const convert = () => {
    const n = new Date().getTime();
    const arr = toBytesInt64(BigInt(n));
    console.log("--- ", n, arr);
    console.log("--- ", fromBytesInt64(arr));

    const x = 1234;
    const arr2 = toBytesInt16(x);
    console.log("--- ", x, arr2);
    console.log("--- ", fromBytesInt16(arr2));
  };

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => connect()}>Connect</button>
        <button onClick={() => send()}>Send</button>
        <button onClick={() => convert()}>convert</button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;
