const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

console.log('API_URL configured:', API_URL);
console.log('NEXT_PUBLIC_API_URL env:', process.env.NEXT_PUBLIC_API_URL);

export class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string = API_URL) {
    this.baseUrl = baseUrl;
    console.log('ApiClient initialized with baseUrl:', this.baseUrl);
  }

  setToken(token: string | null) {
    this.token = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const url = `${this.baseUrl}${endpoint}`;
    console.log(`API Request: ${options.method || 'GET'} ${url}`);
    console.log(`Token present:`, !!this.token);
    if (this.token) {
      console.log(`Token preview:`, this.token.substring(0, 20) + '...');
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      console.log(`API Response: ${response.status} ${response.statusText}`);

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`API Error Response:`, errorText);
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log(`API Success:`, data);
      return data;
    } catch (error) {
      console.error(`API Request Failed:`, error);
      throw error;
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async put<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();
