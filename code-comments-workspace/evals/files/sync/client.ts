export interface SyncRecord {
  id: string;
  payload: unknown;
}

export class SyncClient {
  constructor(private readonly baseUrl: string) {}

  async push(records: SyncRecord[]): Promise<void> {
    const response = await fetch(`${this.baseUrl}/records`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(records),
    });
    if (!response.ok) {
      throw new Error(`push failed: ${response.status}`);
    }
  }
}
