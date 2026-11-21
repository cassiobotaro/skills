export interface SyncRecord {
  id: string;
  payload: unknown;
}

// The API rejects request bodies over 1 MB; our largest records are about 2 KB.
const MAX_RECORDS_PER_REQUEST = 500;

export class SyncClient {
  constructor(private readonly baseUrl: string) {}

  // Batches are sent sequentially; if one fails, earlier batches stay pushed.
  async push(records: SyncRecord[]): Promise<void> {
    for (let i = 0; i < records.length; i += MAX_RECORDS_PER_REQUEST) {
      const batch = records.slice(i, i + MAX_RECORDS_PER_REQUEST);
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
