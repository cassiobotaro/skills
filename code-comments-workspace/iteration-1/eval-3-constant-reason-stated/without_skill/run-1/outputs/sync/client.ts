export interface SyncRecord {
  id: string;
  payload: unknown;
}

// The API rejects request bodies over 1 MB. Our largest records are about
// 2 KB, so 500 records per request stays well under that limit.
const MAX_BATCH_SIZE = 500;

export class SyncClient {
  constructor(private readonly baseUrl: string) {}

  async push(records: SyncRecord[]): Promise<void> {
    for (let i = 0; i < records.length; i += MAX_BATCH_SIZE) {
      await this.pushBatch(records.slice(i, i + MAX_BATCH_SIZE));
    }
  }

  private async pushBatch(batch: SyncRecord[]): Promise<void> {
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
