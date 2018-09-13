import pygame, random, time
pygame.init()
pygame.mixer.init() #INITIALIZATION

screen = pygame.display.set_mode((610, 510))
pygame.display.set_caption("Coffee Shop")

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((25, 20, 25)) #DISPLAY SETTINGS

counterBound = pygame.image.load("counterBound.jpg")
counterBound = pygame.transform.scale(counterBound, (610, 50))

thanks = pygame.mixer.Sound("thankyou.ogg")

menu = ["Hot coffee", "Ice coffee", "Hot chocolate", "Ice chocolate", "Hot tea", "Ice tea"]
prices = {"Hot coffee": 20, "Ice coffee": 20, "Hot chocolate": 30, "Ice chocolate": 35, "Hot tea": 10, "Ice tea": 15}
salesCount = {"Hot coffee": 0, "Ice coffee": 0, "Hot chocolate": 0, "Ice chocolate": 0, "Hot tea": 0, "Ice tea": 0}
customerList = ["customer1", "customer2"]

totalSales = 0
amount = 0
totalSalesDirect =0
# FONT LABELS
orderLabel = pygame.font.SysFont("century gothic", 20)
orderLabel2 = pygame.font.SysFont("league gothic", 20)
salesLabel = pygame.font.SysFont("comic sans", 30)

def Day():
    totalCustomerPerDay = random.randrange(40,100)
    averageTimeSpent = 0
    timeSpent = 0
    global totalSalesDirect

    for i in range(totalCustomerPerDay):
        choicee = random.choice(menu)
        timeSpent += random.randrange(1,20)
        totalSalesDirect += prices[choicee]
    averageTimeSpent += timeSpent/totalCustomerPerDay

    print("=================DAILY===================")
    print("TOTAL REVENUE: ", str(totalSalesDirect))
    print("NO. OF CUSTOMER SERVED PER DAY: ", str(totalCustomerPerDay))
    print("AVERAGE TIME SPENT: ", str(averageTimeSpent))
    print("=========================================")

def Month():
    averageTimeSpent = 0
    timeSpent = 0
    monthlyServing = 0
    global totalSalesDirect

    for j in range(30):
        totalCustomerPerMonth = random.randrange(40, 100)
        monthlyServing += totalCustomerPerMonth
        for i in range(totalCustomerPerMonth):
            choicee = random.choice(menu)
            timeSpent += random.randrange(1, 20)
            totalSalesDirect += prices[choicee]

    averageTimeSpent += timeSpent / monthlyServing

    print("=================MONTHLY=================")
    print("TOTAL REVENUE: ", str(totalSalesDirect))
    print("NO. OF CUSTOMER SERVED PER MONTH: ", str(monthlyServing))
    print("AVERAGE TIME SPENT: ", str(averageTimeSpent))
    print("=========================================")

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
        self.rect.x = 240
        self.rect.y = 530
        self.timee = random.randrange(5, 10)
        self.quantity = random.randrange(1, 15)
        self.order = random.choice(menu)

    def update(self):
        global customerCtr, totalSales, seconds, amount, sales, spawnCust
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
                if (seconds <= 1):
                    self.counterQueue = False
                    self.exitQueue = True

        if self.exitQueue:
            if self.rect.x <= 400:
                self.rect.x += 1
                thanks.play()
            else:
                self.rect.y += 1
                if self.rect.y > 510:
                    self.kill()
                    totalSales += (prices[self.order] * self.quantity)
                    salesCount[self.order] += self.quantity
                    customerCtr += 1
                    thanks.stop()
                    self.exitQueue = False
                    self.waitingQueue = True
                    spawnCust = True

        amount = self.quantity * prices[self.order]

        OrderLabel1 = orderLabel2.render("Order: " + str(self.order), True, (255, 255, 255))
        OrderLabel2 = orderLabel2.render("Quantity: " + str(self.quantity), True, (255, 255, 255))
        OrderLabel3 = orderLabel2.render("Amount: " + str(amount), True, (255, 255, 255))
        servingTime = orderLabel2.render("ORDER/S WILL BE SERVED IN: " + str(self.timee) + " SECOND/S", True,(255, 255, 255))
        totCustLbl = orderLabel2.render("Customer Count: " + str(customerCtr), True, ((250,235,215)))
        
        screen.blit(OrderLabel1, (self.rect.x + 50, self.rect.y + 10))
        screen.blit(OrderLabel2, (self.rect.x + 50, self.rect.y + 30))
        screen.blit(OrderLabel3, (self.rect.x + 50, self.rect.y + 50))
        screen.blit(servingTime, (320, 140))
        screen.blit(totCustLbl, (15, 320))

class Counter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        counter = pygame.image.load("cashier.png")
        customer = pygame.transform.scale(counter, (100, 100))
        self.image = customer
        self.rect = self.image.get_rect()
        self.rect.x = 220
        self.rect.y = 50

    def update(self):
        self.rect.x = 220


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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Day()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                Month()

    screen.blit(background, (0, 0))
    screen.blit(counterBound, (0, 162))

    instruction = orderLabel2.render("INSTRUCTION!", True, (0, 255, 255))
    instruction1 = orderLabel2.render("Press left key for daily computation.", True, (0, 255, 255))
    instruction2 = orderLabel2.render("Press right key for monthly computation.", True, (0, 255, 255))
    salesBreakdown = orderLabel2.render("=== SALES BREAKDOWN ===", True, (255,228,196))
    screen.blit(instruction, (15,230))
    screen.blit(instruction1, (15, 250))
    screen.blit(instruction2, (15, 270))
    screen.blit(salesBreakdown, (15, 300))
    # =================LABELS========================
    itemsDisplay = orderLabel2.render("==== ITEMS SOLD ===", True, (255,228,196))
    totSalesLbl = orderLabel2.render("Total Sales: " + str(totalSales), True, (255,228,196))
    hotCofLbl = orderLabel2.render("Hot Coffee Count: " + str(salesCount["Hot coffee"]), True, (255,228,196))
    iceCofLbl = orderLabel2.render("Ice Coffee Count: " + str(salesCount["Ice coffee"]), True, (255,228,196))
    hotChocLbl = orderLabel2.render("Hot Choco Count: " + str(salesCount["Hot chocolate"]), True, (255,228,196))
    iceChocLbl = orderLabel2.render("Ice Choco Count: " + str(salesCount["Ice chocolate"]), True, (255,228,196))
    hotTea = orderLabel2.render("Hot Tea Count: " + str(salesCount["Hot tea"]), True, (255,228,196))
    iceTea = orderLabel2.render("Ice Tea Count: " + str(salesCount["Ice tea"]), True, (255,228,196))

    screen.blit(itemsDisplay, (15, 360))
    screen.blit(totSalesLbl, (15, 340))

    screen.blit(hotCofLbl, (15, 380))
    screen.blit(iceCofLbl, (15, 400))
    screen.blit(hotChocLbl, (15, 420))
    screen.blit(iceChocLbl, (15, 440))
    screen.blit(hotTea, (15, 460))
    screen.blit(iceTea, (15, 480))

    allSprites.clear(screen, background)
    allSprites.update()
    allSprites.draw(screen)
    pygame.display.update()

pygame.quit()
quit()
