import pygame, random, time
pygame.init()
#hehehehe
screen = pygame.display.set_mode((900, 550))
pygame.display.set_caption("Coffee Shop")

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((25, 20, 25))

counterBound = pygame.image.load("counterBound.jpg")
counterBound = pygame.transform.scale(counterBound, (598, 50))

notif = pygame.image.load("notification.png")
notif = pygame.transform.scale(notif, (50, 50))

menu = ["Hot coffee", "Ice coffee", "Hot chocolate", "Ice chocolate", "Hot tea", "Ice tea"]
prices = {"Hot coffee": 20, "Ice coffee": 20, "Hot chocolate": 30, "Ice chocolate":35, "Hot tea": 10, "Ice tea":15}
salesCount = {"Hot coffee": 0, "Ice coffee": 0, "Hot chocolate": 0, "Ice chocolate":0, "Hot tea": 0, "Ice tea":0}
customerList = ["customer1", "customer2"]

totalSales = 0
amount = 0

orderLabel = pygame.font.SysFont("century gothic", 20)
orderLabel2 = pygame.font.SysFont("league gothic", 20)
salesLabel = pygame.font.SysFont("comic sans", 30)

class Customer(pygame.sprite.Sprite):
    counterQueue = False
    waitingQueue = True
    exitQueue = False
    

    def __init__(self):
        super().__init__()
        customer = pygame.image.load("customer1.png")
        customer = pygame.transform.scale(customer, (50, 50))
        self.image = customer
        self.rect = self.image.get_rect()
        self.rect.x = 230
        self.rect.y = 530
        self.timee = random.randrange(5, 10)
        self.quantity = random.randrange(1, 3)
        self.order = random.choice(menu)

    def update(self):
        global customerCtr, totalSales, notif, seconds, amount, sales, spawnCust
        if self.waitingQueue:
            self.rect.y -= 1
            if self.rect.y < 223:
                self.rect.y = 223
                self.waitingQueue = False
                self.counterQueue = True

        if self.counterQueue:
            for i in range(self.timee):
                seconds = self.timee - i;
                time.sleep(1)
                print(seconds)
                if (seconds <= 1):
                    self.counterQueue = False
                    self.exitQueue = True

        if self.exitQueue:
            self.rect.x = 245
            self.rect.y += 1
            if self.rect.y > 545:
                self.kill()
                totalSales += (prices[self.order] * self.quantity)
                salesCount[self.order] += self.quantity
                customerCtr += 1
                self.timee = 0
                self.exitQueue = False
                self.waitingQueue = True
                spawnCust = True
                print("TOTAL SALES: "+str(totalSales))
                print(salesCount)

        amount = self.quantity * prices[self.order]

        OrderLabel1 = orderLabel2.render("Order: " + str(self.order), True, (255,255,255))
        OrderLabel2 = orderLabel2.render("Quantity: " + str(self.quantity), True, (255, 255, 255))
        OrderLabel3 = orderLabel2.render("Amount: " + str(amount), True, (255, 255, 255))
        servingTime = orderLabel2.render("ORDER/S WILL BE SERVED IN: " + str(self.timee) + " SECOND/S", True, (255, 255, 255))

        screen.blit(OrderLabel1, (self.rect.x+50, self.rect.y + 10))
        screen.blit(OrderLabel2, (self.rect.x + 50, self.rect.y + 30))
        screen.blit(OrderLabel3, (self.rect.x + 50, self.rect.y + 50))
        screen.blit(servingTime, (300, 140))
        screen.blit(totCustLbl, (667, 247))

class Counter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        counter = pygame.image.load("cashier.png")
        customer = pygame.transform.scale(counter, (100, 100))
        self.image = customer
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 50

    def update(self):
        self.rect.x = 200

done = True
spawnCust = True
clock = pygame.time.Clock()
allSprites = pygame.sprite.Group()
customers_ = pygame.sprite.Group()
counter_ = pygame.sprite.Group()

customers = Customer()
counter = Counter()

allSprites.add(counter)
customers_.add(customers)
counter_.add(counter)
customerCtr = 0
while done:

    if spawnCust:
        customers = Customer()
        customers_.add(customers)
        allSprites.add(customers)
        spawnCust = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())

    screen.blit(background, (0,0))
    screen.blit(counterBound, (0, 162))
    #=================LABELS========================
    itemsSoldLbl = orderLabel.render("==== ITEMS SOLD ===", True, (0, 255, 255))
    totCustLbl = orderLabel.render("Customer Count: " + str(customerCtr), True, (0, 255, 255))

    screen.blit(totCustLbl, (667, 270))

    allSprites.clear(screen, background)
    allSprites.update()
    allSprites.draw(screen)
    pygame.display.update()

pygame.quit()
quit()
