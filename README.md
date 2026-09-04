# Copy Cookies — Chrome Extension

Extension đơn giản: bấm icon → popup hiện 2 nút **Copy** và **Paste**.

## Chức năng
- **Copy cookies**: lấy toàn bộ cookie của tab đang mở, ghi ra clipboard dưới dạng JSON.
- **Paste cookies**: đọc JSON cookie từ clipboard và set lại vào tab hiện tại.

## Cài đặt (chế độ Developer)
1. Mở Chrome → `chrome://extensions`
2. Bật **Developer mode** (góc trên bên phải)
3. Bấm **Load unpacked** → chọn thư mục `copy-cookies`
4. Ghim icon extension lên thanh công cụ nếu muốn

## Cách dùng
1. Mở trang web cần thao tác cookie
2. Bấm icon extension → popup hiện ra
3. Bấm **Copy cookies** để sao chép, hoặc **Paste cookies** để dán

## Cài đặt (Settings)
Bấm icon ⚙ ở góc phải popup để bật/tắt các tính năng (lưu qua `chrome.storage.local`):

**Khi Copy**
- **Gồm subdomain & domain cha** — lấy cả cookie ở subdomain khác (vd `api.…`) và domain cha (`.example.com`), không chỉ cookie khớp URL. *(mặc định: bật)*
- **Gồm cookie Partitioned (CHIPS)** — lấy cả cookie bị ngăn hộc theo site top-level. *(bật)*

**Khi Paste**
- **Remap sang tab hiện tại** — nếu dán sang host khác họ domain (vd `localhost`) thì gán cookie về host đó. Tắt = luôn khôi phục domain gốc. *(bật)*
- **Chỉ lấy cookie cùng họ app** — khi remap, bỏ subdomain lạc và khử trùng theo tên. Tắt = dán mọi cookie. *(bật)*
- **Bỏ cờ Secure trên http** — cho phép ghi cookie trên `http://localhost`. Tắt = giữ Secure (có thể set thất bại trên http). *(bật)*

## Cấu trúc
```
copy-cookies/
├── manifest.json     # cấu hình extension (MV3)
├── popup.html        # giao diện popup
├── popup.css         # style (theme Hextech / LMHT)
├── popup.js          # logic copy/paste cookie
└── icons/            # icon 16/48/128 (+ src/: SVG nguon & script sinh lai)
```

## Giao diện
Popup dùng theme **Hextech** lấy cảm hứng từ client Liên Minh Huyền Thoại: nền navy–đen, viền vàng với 4 góc trang trí, chữ hoa giãn cách theo font display, checkbox hình thoi và hiệu ứng phát sáng xanh ngọc khi thao tác thành công. Icon extension cũng theo tông này: khung lục giác vàng, lõi pha lê xanh ngọc (bản 16px rút gọn còn 1 lõi cho dễ nhìn trên thanh công cụ) — sinh lại bằng `python3 icons/src/generate-icons.py`. Toàn bộ style nằm trong `popup.css` (không phụ thuộc font/ảnh bên ngoài nên hợp CSP của MV3).

## Lưu ý
- Chỉ hoạt động trên trang `http://` và `https://`.
- Cookie `httpOnly` vẫn copy được (do dùng API `chrome.cookies`), nhưng khi paste sang domain khác có thể bị chặn tùy chính sách `SameSite`/`Secure`.
- Cookie session (không có ngày hết hạn) sẽ được set dưới dạng session cookie.
# copy-cookies
