import tkinter as tk  # Import library tkinter untuk GUI
import random # Import library random untuk fitur power-up

# Kelas dasar untuk semua objek dalam permainan
class GameObject(object):
    def __init__(self, canvas, item):  # Inisialisasi objek permainan
        self.canvas = canvas  # Kanvas tempat objek berada
        self.item = item  # Objek itu sendiri (dalam kanvas)

    def get_position(self):  # Mendapatkan posisi objek
        return self.canvas.coords(self.item)

    def move(self, x, y):  # Memindahkan objek
        self.canvas.move(self.item, x, y)

    def delete(self):  # Menghapus objek
        self.canvas.delete(self.item)

# Kelas bola dalam permainan
class Ball(GameObject):
    def __init__(self, canvas, x, y):  # Inisialisasi bola
        self.radius = 10  # Radius bola
        self.direction = [1, -1]  # Arah awal bola
        self.speed = 5  # Kecepatan awal bola
        # Membuat bola sebagai lingkaran di kanvas
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='white')
        super(Ball, self).__init__(canvas, item)  # Memanggil konstruktor kelas induk

    def update(self):  # Update posisi bola
        coords = self.get_position()  # Dapatkan posisi bola
        width = self.canvas.winfo_width()  # Lebar kanvas
        # Pantulan jika bola menyentuh sisi kiri atau kanan
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        # Pantulan jika bola menyentuh sisi atas
        if coords[1] <= 0:
            self.direction[1] *= -1
        # Hitung pergerakan bola
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)  # Gerakkan bola

    def collide(self, game_objects):  # Periksa tabrakan bola dengan objek lain
        coords = self.get_position()  # Dapatkan posisi bola
        x = (coords[0] + coords[2]) * 0.5  # Hitung titik tengah bola
        # Pantulan vertikal jika mengenai lebih dari satu objek
        if len(game_objects) > 1:
            self.direction[1] *= -1
        elif len(game_objects) == 1:  # Pantulan horizontal jika hanya satu objek
            game_object = game_objects[0]
            coords = game_object.get_position()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1
        # Hit jika objek adalah batu bata
        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()

# Kelas paddle dalam permainan
class Paddle(GameObject):
    def __init__(self, canvas, x, y):  # Inisialisasi paddle
        self.width = 80  # Lebar paddle
        self.height = 10  # Tinggi paddle
        self.ball = None  # Referensi ke bola
        # Membuat paddle sebagai persegi panjang di kanvas
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='#FFB643')
        super(Paddle, self).__init__(canvas, item)  # Memanggil konstruktor kelas induk

    def set_ball(self, ball):  # Menghubungkan paddle dengan bola
        self.ball = ball

    def move(self, offset):  # Gerakkan paddle ke kiri atau kanan
        coords = self.get_position()  # Dapatkan posisi paddle
        width = self.canvas.winfo_width()  # Lebar kanvas
        # Pastikan paddle tidak keluar dari kanvas
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)  # Panggil metode gerak kelas induk
            if self.ball is not None:  # Jika bola ada di paddle, gerakkan bola juga
                self.ball.move(offset, 0)

    def enlarge(self):  # Tambahkan lebar paddle (power-up)
        self.width += 20  # Tambahkan lebar paddle
        coords = self.get_position()  # Dapatkan posisi paddle
        # Update koordinat paddle di kanvas
        self.canvas.coords(self.item, coords[0], coords[1], coords[0] + self.width, coords[3])

# Kelas batu bata (Brick)
class Brick(GameObject):
    COLORS = {1: '#4535AA', 2: '#ED639E', 3: '#8FE1A2'}  # Warna berdasarkan jumlah hit

    def __init__(self, canvas, x, y, hits):  # Inisialisasi brick
        self.width = 75  # Lebar brick
        self.height = 20  # Tinggi brick
        self.hits = hits  # Jumlah hit yang diperlukan untuk menghancurkan
        color = Brick.COLORS[hits]  # Pilih warna berdasarkan jumlah hit
        # Membuat brick sebagai persegi panjang di kanvas
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)  # Memanggil konstruktor kelas induk

    def hit(self):  # Kurangi hit saat terkena bola
        self.hits -= 1  # Kurangi jumlah hit
        if self.hits == 0:  # Jika hit habis, hapus brick
            self.delete()
        else:  # Jika tidak, ubah warna brick
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])

# ** Lanjutan kode kelas permainan dan implementasi level, power-up, dan kecepatan bola. **
import tkinter as tk  # Import library tkinter untuk GUI
import random  # Import library random untuk fitur power-up

# Kelas dasar untuk semua objek dalam permainan
class GameObject(object):
    def __init__(self, canvas, item):  # Inisialisasi objek permainan
        self.canvas = canvas  # Kanvas tempat objek berada
        self.item = item  # Objek itu sendiri (dalam kanvas)

    def get_position(self):  # Mendapatkan posisi objek
        return self.canvas.coords(self.item)

    def move(self, x, y):  # Memindahkan objek
        self.canvas.move(self.item, x, y)

    def delete(self):  # Menghapus objek
        self.canvas.delete(self.item)

# Kelas bola dalam permainan
class Ball(GameObject):
    def __init__(self, canvas, x, y):  # Inisialisasi bola
        self.radius = 10  # Radius bola
        self.direction = [1, -1]  # Arah awal bola
        self.speed = 5  # Kecepatan awal bola
        # Membuat bola sebagai lingkaran di kanvas
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='white')
        super(Ball, self).__init__(canvas, item)  # Memanggil konstruktor kelas induk

    def update(self):  # Update posisi bola
        coords = self.get_position()  # Dapatkan posisi bola
        width = self.canvas.winfo_width()  # Lebar kanvas
        # Pantulan jika bola menyentuh sisi kiri atau kanan
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        # Pantulan jika bola menyentuh sisi atas
        if coords[1] <= 0:
            self.direction[1] *= -1
        # Hitung pergerakan bola
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)  # Gerakkan bola

    def collide(self, game_objects):  # Periksa tabrakan bola dengan objek lain
        coords = self.get_position()  # Dapatkan posisi bola
        x = (coords[0] + coords[2]) * 0.5  # Hitung titik tengah bola
        # Pantulan vertikal jika mengenai lebih dari satu objek
        if len(game_objects) > 1:
            self.direction[1] *= -1
        elif len(game_objects) == 1:  # Pantulan horizontal jika hanya satu objek
            game_object = game_objects[0]
            coords = game_object.get_position()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1
        # Hit jika objek adalah batu bata
        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()

# Kelas paddle dalam permainan
class Paddle(GameObject):
    def __init__(self, canvas, x, y):  # Inisialisasi paddle
        self.width = 80  # Lebar paddle
        self.height = 10  # Tinggi paddle
        self.ball = None  # Referensi ke bola
        # Membuat paddle sebagai persegi panjang di kanvas
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='#FFB643')
        super(Paddle, self).__init__(canvas, item)  # Memanggil konstruktor kelas induk

    def set_ball(self, ball):  # Menghubungkan paddle dengan bola
        self.ball = ball

    def move(self, offset):  # Gerakkan paddle ke kiri atau kanan
        coords = self.get_position()  # Dapatkan posisi paddle
        width = self.canvas.winfo_width()  # Lebar kanvas
        # Pastikan paddle tidak keluar dari kanvas
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)  # Panggil metode gerak kelas induk
            if self.ball is not None:  # Jika bola ada di paddle, gerakkan bola juga
                self.ball.move(offset, 0)

    def enlarge(self):  # Tambahkan lebar paddle (power-up)
        self.width += 20  # Tambahkan lebar paddle
        coords = self.get_position()  # Dapatkan posisi paddle
        # Update koordinat paddle di kanvas
        self.canvas.coords(self.item, coords[0], coords[1], coords[0] + self.width, coords[3])

# Kelas batu bata (Brick)
class Brick(GameObject):
    COLORS = {1: '#4535AA', 2: '#ED639E', 3: '#8FE1A2'}  # Warna berdasarkan jumlah hit

    def __init__(self, canvas, x, y, hits):  # Inisialisasi brick
        self.width = 75  # Lebar brick
        self.height = 20  # Tinggi brick
        self.hits = hits  # Jumlah hit yang diperlukan untuk menghancurkan
        color = Brick.COLORS[hits]  # Pilih warna berdasarkan jumlah hit
        # Membuat brick sebagai persegi panjang di kanvas
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)  # Memanggil konstruktor kelas induk

    def hit(self):  # Kurangi hit saat terkena bola
        self.hits -= 1  # Kurangi jumlah hit
        if self.hits == 0:  # Jika hit habis, hapus brick
            self.delete()
        else:  # Jika tidak, ubah warna brick
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])

class Game(tk.Frame):  # Kelas utama untuk permainan
    def __init__(self, master):  # Inisialisasi permainan
        super(Game, self).__init__(master)  # Panggil konstruktor kelas induk
        self.level = 1  # Level awal permainan
        self.lives = 3  # Nyawa pemain
        self.width = 610  # Lebar kanvas
        self.height = 400  # Tinggi kanvas
        self.canvas = tk.Canvas(self, bg='#D6D1F5', width=self.width, height=self.height)  # Buat kanvas
        self.canvas.pack()  # Tambahkan kanvas ke frame
        self.pack()  # Tambahkan frame ke master

        self.items = {}  # Penyimpanan objek permainan
        self.ball = None  # Referensi bola
        self.paddle = Paddle(self.canvas, self.width / 2, 326)  # Buat paddle
        self.items[self.paddle.item] = self.paddle  # Tambahkan paddle ke item

        # Tambahkan batu bata ke level awal
        self.add_bricks()

        self.hud = None  # Heads-up display (HUD) untuk nyawa
        self.setup_game()  # Setup permainan
        self.canvas.focus_set()  # Fokus pada kanvas
        # Bind kontrol untuk paddle
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-20))  # Gerakkan paddle ke kiri
        self.canvas.bind('<Right>', lambda _: self.paddle.move(20))  # Gerakkan paddle ke kanan

    def add_bricks(self):  # Tambahkan batu bata untuk level
        for x in range(5, self.width - 5, 75):  # Iterasi posisi x
            for y in range(50, 50 + (self.level * 20), 20):  # Iterasi posisi y berdasarkan level
                hits = random.choice([1, 2, 3])  # Jumlah hit acak
                self.add_brick(x + 37.5, y, hits)  # Tambahkan brick

    def setup_game(self):  # Setup permainan baru
        self.add_ball()  # Tambahkan bola
        self.update_lives_text()  # Perbarui HUD nyawa
        self.text = self.draw_text(300, 200, f'Level {self.level}\nPress Space to start')  # Tampilkan teks level
        self.canvas.bind('<space>', lambda _: self.start_game())  # Bind tombol Space untuk memulai

    def add_ball(self):  # Tambahkan bola ke permainan
        if self.ball is not None:  # Jika bola sudah ada, hapus
            self.ball.delete()
        paddle_coords = self.paddle.get_position()  # Dapatkan posisi paddle
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5  # Posisi bola di tengah paddle
        self.ball = Ball(self.canvas, x, 310)  # Buat bola baru
        self.paddle.set_ball(self.ball)  # Hubungkan bola dengan paddle

    def add_brick(self, x, y, hits):  # Tambahkan brick ke permainan
        brick = Brick(self.canvas, x, y, hits)  # Buat brick
        self.items[brick.item] = brick  # Tambahkan ke penyimpanan item

    def draw_text(self, x, y, text, size='40'):  # Gambar teks pada kanvas
        font = ('Forte', size)  # Gunakan font Forte
        return self.canvas.create_text(x, y, text=text, font=font)  # Kembalikan ID teks

    def update_lives_text(self):  # Perbarui tampilan nyawa
        text = f'Lives: {self.lives}'  # Format teks nyawa
        if self.hud is None:  # Jika HUD belum ada, buat
            self.hud = self.draw_text(50, 20, text, 15)
        else:  # Jika HUD sudah ada, perbarui teks
            self.canvas.itemconfig(self.hud, text=text)

    def start_game(self):  # Memulai permainan
        self.canvas.unbind('<space>')  # Hapus bind tombol Space
        self.canvas.delete(self.text)  # Hapus teks start
        self.paddle.ball = None  # Pisahkan bola dari paddle
        self.game_loop()  # Mulai game loop

    def game_loop(self):  # Loop utama permainan
        self.check_collisions()  # Periksa tabrakan
        num_bricks = len(self.canvas.find_withtag('brick'))  # Hitung sisa brick
        if num_bricks == 0:  # Jika semua brick hancur
            self.level += 1  # Naik level
            self.ball.speed += 2  # Tambahkan kecepatan bola
            self.setup_game()  # Setup permainan untuk level baru
        elif self.ball.get_position()[3] >= self.height:  # Jika bola jatuh ke bawah
            self.lives -= 1  # Kurangi nyawa
            if self.lives < 0:  # Jika nyawa habis
                self.draw_text(300, 200, 'Game Over')  # Tampilkan Game Over
            else:  # Jika masih ada nyawa
                self.after(1000, self.setup_game)  # Restart permainan setelah 1 detik
        else:  # Jika tidak, teruskan permainan
            self.ball.update()  # Update posisi bola
            self.after(50, self.game_loop)  # Lanjutkan loop setelah 50ms

    def check_collisions(self):  # Periksa tabrakan antara bola dan objek lain
        ball_coords = self.ball.get_position()  # Dapatkan posisi bola
        items = self.canvas.find_overlapping(*ball_coords)  # Dapatkan item yang bertabrakan
        objects = [self.items[x] for x in items if x in self.items]  # Filter objek valid
        self.ball.collide(objects)  # Proses tabrakan dengan bola

        # Power-up: jika paddle terkena brick
        for obj in objects:
            if isinstance(obj, Brick) and random.random() < 0.2:  # 20% peluang
                self.paddle.enlarge()  # Perbesar paddle (power-up)

# Main program
if __name__ == '__main__':
    root = tk.Tk()  # Buat root window
    root.title('Break those Bricks!')  # Judul aplikasi
    game = Game(root)  # Buat instance permainan
    game.mainloop()  # Jalankan loop utama aplikasi
