export interface SyncRecord {
  id: string;
  payload: unknown;
}

// The API rejects request bodies over 1 MB. Our largest records are about 2 KB,
// so batches of at most 500 stay under that limit.
const MAX_RECORDS_PER_REQUEST = 500;

export class SyncClient {
  constructor(private readonly baseUrl: string) {}

  async push(records: SyncRecord[]): Promise<void> {
    for (let i = 0; i < records.length; i += MAX_RECORDS_PER_REQUEST) {
      await this.pushBatch(records.slice(i, i + MAX_RECORDS_PER_REQUEST));
    }
  }

  private async pushBatch(records: SyncRecord[]): Promise<void> {
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
