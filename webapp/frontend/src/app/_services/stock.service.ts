import { Injectable } from '@angular/core';
import axios from 'axios';

@Injectable({
  providedIn: 'root'
})
export class StockService {
  private apiKey = 'AORMSJJL3MBAG177'; // Remplacez YOUR_API_KEY par votre clé API Alpha Vantage

  public async getStockData(symbol: string): Promise<any> {
    const apiUrl = `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=${symbol}&apikey=${this.apiKey}`;
    const response = await axios.get(apiUrl);
    return response.data;
  }
}
