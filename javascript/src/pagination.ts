import { HttpClient } from "./http";
import type { PaginatedResponse } from "./types";

export class AutoPaginator<T> implements AsyncIterableIterator<T> {
  private currentPage = 1;
  private currentItems: T[] = [];
  private itemIndex = 0;
  private totalPages = 1;
  private hasNext = true;
  private hasFetchedFirstPage = false;

  constructor(
    private http: HttpClient,
    private path: string,
    private baseParams: Record<string, string | number | undefined> = {},
    private limit = 50,
    private options: {
      pageParam?: string;
      perPageParam?: string;
      pageKey?: string;
      perPageKey?: string;
      totalKey?: string;
    } = {},
  ) {}

  private async fetchNextPage(): Promise<boolean> {
    if (this.hasFetchedFirstPage && !this.hasNext) {
      return false;
    }

    const params = {
      ...this.baseParams,
      [this.options.pageParam ?? "pagina"]: this.hasFetchedFirstPage ? this.currentPage + 1 : this.currentPage,
      [this.options.perPageParam ?? "limite"]: this.limit,
    };

    const response = await this.http.get<PaginatedResponse<T>>(this.path, params);
    const envelope = response as PaginatedResponse<T> & Record<string, unknown>;

    this.currentItems = response.items;
    const pageKey = this.options.pageKey ?? "pagina";
    const perPageKey = this.options.perPageKey ?? "limite";
    this.currentPage = Number(envelope[pageKey] ?? 1);
    this.totalPages = Number(envelope.paginas ?? 1);
    const totalKey = this.options.totalKey;
    this.hasNext = totalKey
      ? this.currentPage * Number(envelope[perPageKey] ?? this.limit) < Number(envelope[totalKey] ?? 0)
      : this.currentPage < this.totalPages;
    this.itemIndex = 0;
    this.hasFetchedFirstPage = true;

    return this.currentItems.length > 0;
  }

  async next(): Promise<IteratorResult<T>> {
    if (this.itemIndex >= this.currentItems.length) {
      const hasMore = await this.fetchNextPage();
      if (!hasMore) {
        return { value: undefined as unknown as T, done: true };
      }
    }

    const value = this.currentItems[this.itemIndex++];
    return { value, done: false };
  }

  [Symbol.asyncIterator](): AsyncIterableIterator<T> {
    return this;
  }
}
