export interface SyncRecord {
  id: string;
  payload: unknown;
}

// The API rejects request bodies over 1 MB. Our largest records are about
// 2 KB, so 500 per batch (~1 MB worst case) stays under the limit.
const MAX_BATCH_SIZE = 500;

export class SyncClient {
  constructor(private readonly baseUrl: string) {}

  async push(records: SyncRecord[]): Promise<void> {
    for (let i = 0; i < records.length; i += MAX_BATCH_SIZE) {
      const batch = records.slice(i, i + MAX_BATCH_SIZE);
      const response = await fetch(`${this.baseUrl}/records`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(batch),
      });
      if (!response.ok) {
        throw new Error(`push failed: ${response.status}`);
      }
    }
  }
}
