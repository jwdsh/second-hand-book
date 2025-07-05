import csv
import time
import requests
import statistics  # 新增：替代numpy的内置库
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pathlib import Path
from config import INPUT_FILE, OUTPUT_FILE, IMAGE_DIR


class DangDangCrawler:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.results = []

    def get_random_headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'http://www.dangdang.com/',
            'DNT': '1',
            'Connection': 'keep-alive'
        }

    def search_books(self, keyword, max_retries=3):
        """搜索当当网书籍（带重试机制）"""
        url = f"http://search.dangdang.com/?key={keyword}&act=input"
        print(f"正在搜索: {keyword}")

        for attempt in range(max_retries):
            try:
                response = self.session.get(
                    url,
                    headers=self.get_random_headers(),
                    timeout=10
                )
                if "验证" in response.text or "security" in response.url.lower():
                    raise Exception("触发反爬验证")
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response.text
            except Exception as e:
                print(f"搜索失败（尝试 {attempt + 1}/{max_retries}）: {e}")
                time.sleep(5 * (attempt + 1))
        return None

    def parse_search_results(self, html, keyword):
        """解析搜索结果（简化版）"""
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        items = soup.select('ul.bigimg li, ul.smallimg li')
        books = []

        for item in items:
            try:
                title_elem = (item.select_one('a[dd_name="单品标题"]') or
                              item.select_one('a.pic') or
                              item.select_one('a[name="itemlist-title"]'))
                title = title_elem.get('title', '').strip() or title_elem.text.strip()

                price_elem = (item.select_one('p.price span.search_now_price') or
                              item.select_one('span.price_n'))
                price = price_elem.text.strip().replace('¥', '').replace('￥', '').strip()

                img_elem = item.select_one('img')
                img_url = (img_elem.get('data-original') or
                           img_elem.get('src') if img_elem else '')

                img_path = self.download_image(img_url, title) if img_url else ''

                books.append({
                    'title': title,
                    'price': float(price) if price.replace('.', '').isdigit() else 0.0,
                    'image_path': str(img_path) if img_path else ''
                })
            except Exception as e:
                print(f"解析条目失败（跳过）：{e}")
                continue
        return books

    def download_image(self, img_url, title):
        """下载书籍图片"""
        if not img_url:
            return ''

        try:
            if img_url.startswith('//'):
                img_url = 'http:' + img_url
            safe_title = ''.join(c if c.isalnum() else '_' for c in title.encode('utf-8').decode('utf-8', 'ignore'))[:50]
            img_name = f"{safe_title}_{int(time.time())}.jpg"
            img_path = IMAGE_DIR / img_name

            response = self.session.get(
                img_url,
                headers=self.get_random_headers(),
                stream=True,
                timeout=10
            )
            response.raise_for_status()

            with open(img_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return img_path
        except Exception as e:
            print(f"图片下载失败: {e}")
            return ''

    def save_results(self):
        """保存原始数据到results.csv"""
        if not self.results:
            print("没有结果可保存")
            return

        try:
            OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['title', 'price'])
                writer.writeheader()
                writer.writerows([{'title': item['title'], 'price': item['price']} for item in self.results])
            print(f"简版结果已保存到: {OUTPUT_FILE}")
        except Exception as e:
            print(f"保存失败: {e}")
            print("\n以下是应保存的数据：")
            for item in self.results:
                print(f"书名: {item['title']}, 价格: {item['price']}")

    # ============== 以下是新增的两个方法 ==============
    def process_results(self):
        """处理数据：过滤异常值并计算平均价格（不使用numpy）"""
        if not self.results:
            print("没有结果可处理")
            return None

        prices = [item['price'] for item in self.results if item['price'] > 0]
        if not prices:
            print("没有有效的价格数据")
            return None

        try:
            mean_price = statistics.mean(prices)
            std_price = statistics.stdev(prices) if len(prices) > 1 else 0
            filtered_prices = [p for p in prices if mean_price - 2*std_price <= p <= mean_price + 2*std_price]
            avg_price = statistics.mean(filtered_prices) if filtered_prices else 0
        except statistics.StatisticsError as e:
            print(f"统计计算错误: {e}")
            return None

        return {
            'title': self.results[0]['title'],
            'average_price': round(avg_price, 2)
        }

    def save_processed_results(self, data):
        """保存处理后的结果到processed_results.txt"""
        if not data:
            return

        # 修复：使用 OUTPUT_FILE 的父目录作为输出路径
        processed_file = OUTPUT_FILE.parent / 'processed_results.txt'
        try:
            with open(processed_file, 'w', encoding='utf-8') as f:
                f.write(f"书名: {data['title']}\n")
                f.write(f"平均价格: ¥{data['average_price']:.2f}\n")
            print(f"处理后的结果已保存到: {processed_file}")
        except Exception as e:
            print(f"保存处理结果失败: {e}")

    def run(self):
        """主运行方法（修改：新增处理结果步骤）"""
        if not INPUT_FILE.exists():
            print(f"输入文件不存在: {INPUT_FILE}")
            return

        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            keywords = [line.strip() for line in f if line.strip()]

        if not keywords:
            print("输入文件中没有有效的搜索关键词")
            return

        for keyword in keywords:
            html = self.search_books(keyword)
            books = self.parse_search_results(html, keyword)
            self.results.extend(books)
            time.sleep(2)

        self.save_results()  # 保存原始数据
        processed_data = self.process_results()  # 新增：处理数据
        self.save_processed_results(processed_data)  # 新增：保存处理结果


if __name__ == '__main__':
    crawler = DangDangCrawler()
    crawler.run()