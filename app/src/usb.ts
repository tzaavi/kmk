export class Usb {
  private device?: HIDDevice;

  async connect() {
    const devices = await navigator.hid.requestDevice({ filters: [] });
    if (devices.length > 0) {
      const device = devices[0];
      console.log("device: ", device);
      device.open();
      this.device = device;
    }
  }

  send(msg: unknown) {
    const json = JSON.stringify(msg);
    const encoder = new TextEncoder();
    const bytes = encoder.encode(json);

    const chunks: Uint8Array[] = [];
    for (let i = 0; i < bytes.length; i += 51) {
      const chunk = bytes.slice(i, i + 51);
      chunks.push(chunk);
    }

    const msgId = toBytesInt64(BigInt(new Date().getTime()));
    for (let i = 0; i < chunks.length; i++) {
      const contentSize = toBytesInt16(chunks[0].length);
      const chunksLeft = toBytesInt16(chunks.length - i);
      const data = new Uint8Array(63);
      data.set(msgId, 0);
      data.set(contentSize, 8);
      data.set(chunksLeft, 10);
      data.set(chunks[i], 12);
      console.log("data: ", data.length, data);
      this.device?.sendReport(0x08, data);
    }
  }
}

export const usb = new Usb();

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
