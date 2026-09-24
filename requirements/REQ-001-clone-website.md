---

id: REQ-001
title: Clone Biệt Đội Săn Hàng E-commerce Website
status: ANALYZED
revision: 1
content_hash: e27d9f3d0e4b4f48
priority: CRITICAL
owner:
design: docs/design/REQ-001-design.md
tasks: [TASK-001, TASK-002, TASK-003, TASK-004, TASK-005, TASK-006, TASK-007, TASK-008, TASK-009, TASK-010, TASK-011, TASK-012, TASK-013]
updated: 2026-09-24 09:15
--------

## Goal

Build a functional e-commerce website that reproduces the publicly visible user experience and core functionality of:

https://bietdoisanhang.vn/

The goal is to use the website as a reference implementation and validate whether the Agentic Engineering Team can analyze, design, implement, test, and deliver a multi-page e-commerce application from a single requirement.

The cloned application must reproduce the major navigation structure, page types, product browsing experience, product detail experience, search, cart, and customer-facing flows of the reference website.

The implementation must use independently created application code and assets or assets that are legally available for reuse.

## Scope

### 1. Website structure

Implement the major publicly visible sections of the reference website:

* Home page.
* Product listing page.
* Product category pages.
* Product detail page.
* Search page.
* Shopping cart.
* Login page.
* Registration page.
* News/blog listing.
* News/blog detail.
* About page.
* Contact page.
* Shipping policy page.
* Privacy policy page.
* Return/warranty policy page.
* Terms of service page.
* Shopping guide page.

The reference website currently exposes product categories including fishing bait and fishing equipment/accessories, as well as news and customer-support pages.

### 2. Home page

Reproduce the major user-facing sections:

* Header.
* Navigation menu.
* Product categories.
* Featured/best-selling products.
* Product cards.
* Product pricing.
* Product images.
* News section.
* Customer support/contact information.
* Footer.
* Search entry point.
* Cart entry point.
* Login/register entry points.

The reference homepage contains navigation for products, fishing-bait categories, fishing accessories, news, search, cart, login and registration.

### 3. Product catalog

Users must be able to:

* View products.
* Browse products by category.
* View product name.
* View product image.
* View product price.
* Open product details.
* Navigate between product categories.
* Search for products.

The reference website exposes product categories such as:

* Câu Cá Rô Phi.
* Câu Cá Chép.
* Câu Cá Diếc.
* Câu Cá Trắm Cỏ.
* Câu Cá Trắm Đen.
* Hương Liệu Dụ Cá.
* Dụng Cụ & Phụ Kiện Câu Cá.
* Cần Câu Cá.
* Thẻo Câu Cá.
* Trục Câu Cá.
* Phao Câu Cá.

### 4. Product detail

A product detail page must support:

* Product name.
* Product images.
* Price.
* Product description.
* Product information.
* Usage instructions where applicable.
* Product category.
* Add-to-cart action.
* Quantity selection.
* Related products where appropriate.

Product pages on the reference website contain product information, usage instructions, product metadata and customer contact/support information.

### 5. Shopping cart

Users must be able to:

* Add a product to cart.
* Change quantity.
* Remove a product.
* View cart subtotal.
* View total quantity.
* View total price.
* Continue shopping.
* Proceed to checkout.

### 6. Search

Users must be able to:

* Search products by keyword.
* View matching products.
* Open a matching product.
* Handle zero-result searches gracefully.

### 7. Authentication

Implement basic customer authentication UI and backend functionality:

* Register.
* Login.
* Logout.
* Maintain authenticated session.
* Display appropriate authenticated/unauthenticated navigation.

Authentication does not need to reproduce the implementation of the reference website.

### 8. News

Users must be able to:

* View news/blog listing.
* Open a news article.
* View article title.
* View article content.
* View article image where available.
* Navigate between articles.

The reference website currently exposes a news section with fishing-related articles.

### 9. Static information pages

Implement:

* About.
* Contact.
* Shipping and inspection policy.
* Privacy policy.
* Warranty and return policy.
* Terms of service.
* Shopping guide.

### 10. Responsive UI

The website must support:

* Desktop.
* Tablet.
* Mobile.

Navigation and product layouts must adapt to the viewport.

### 11. Customer support

Provide customer-facing contact actions similar in purpose to the reference site:

* Hotline.
* Contact information.
* Zalo/contact link where configured.
* Footer support links.

Do not copy private customer information or credentials from the reference website.

### 12. Backend

Provide REST APIs for:

* Products.
* Categories.
* Product search.
* Cart.
* Authentication.
* News/articles.
* Customer-facing static content where appropriate.

### 13. Database

Persist at minimum:

* Users.
* Products.
* Categories.
* Product images/URLs.
* Product descriptions.
* Cart.
* Cart items.
* News/articles.

### 14. Testing

Provide:

* Backend unit tests.
* Backend integration tests.
* API tests.
* Frontend component tests.
* Frontend interaction tests.
* End-to-end tests for critical customer flows.

## Out of Scope

The first version does not need to implement:

* Real payment gateway integration.
* Real shipping provider integration.
* Real warehouse management.
* Real ERP integration.
* Real accounting integration.
* Real customer support/chat backend.
* Real SMS/email provider integration.
* Admin CMS unless required by the SA design.
* Product supplier management.
* Marketplace integration.
* Social media management.
* Exact replication of the original website's backend implementation.
* Copying private data, credentials, analytics configuration, tracking identifiers, or customer information.
* Copying copyrighted images or content unless the assets are provided or legally reusable.

## User Stories / Behaviour

* As a visitor, I want to view the homepage so that I can discover products and website content.
* As a visitor, I want to browse product categories so that I can find products relevant to my needs.
* As a visitor, I want to search for products so that I can quickly find a specific product.
* As a visitor, I want to view product details so that I can understand the product before purchasing.
* As a customer, I want to add products to my cart so that I can prepare an order.
* As a customer, I want to change product quantities in my cart so that I can control the items I intend to purchase.
* As a customer, I want to remove products from my cart so that I can correct my purchase selection.
* As a customer, I want to register an account so that I can use customer features.
* As a customer, I want to log in so that the application can identify my account.
* As a visitor, I want to read news articles so that I can learn about products and fishing techniques.
* As a visitor, I want to view contact and policy pages so that I can understand how the business operates.
* As a mobile user, I want the website to work correctly on my phone so that I can browse products conveniently.

## Acceptance Criteria (business level)

### Website

* [ ] AC-001: The homepage is accessible and renders successfully.
* [ ] AC-002: The homepage contains header, navigation, product sections, news section and footer.
* [ ] AC-003: The primary navigation allows users to access the major website sections.
* [ ] AC-004: The website is responsive on desktop, tablet and mobile viewport sizes.

### Products

* [ ] AC-005: Users can view the product catalog.
* [ ] AC-006: Users can browse products by category.
* [ ] AC-007: Product cards display at minimum product name, image and price.
* [ ] AC-008: Users can open a product detail page.
* [ ] AC-009: Product detail pages display product information and description.
* [ ] AC-010: Users can add a product to the shopping cart.
* [ ] AC-011: Users can select or change product quantity before adding to cart.
* [ ] AC-012: Users can view related/recommended products where applicable.

### Search

* [ ] AC-013: Users can search products by keyword.
* [ ] AC-014: Search results contain products matching the search criteria.
* [ ] AC-015: A search with no matching product displays an appropriate empty state.

### Cart

* [ ] AC-016: Users can view the shopping cart.
* [ ] AC-017: Users can increase product quantity in the cart.
* [ ] AC-018: Users can decrease product quantity in the cart.
* [ ] AC-019: Users can remove products from the cart.
* [ ] AC-020: Cart total quantity is calculated correctly.
* [ ] AC-021: Cart total price is calculated correctly.
* [ ] AC-022: Cart state is preserved according to the application's authentication/session design.

### Authentication

* [ ] AC-023: A visitor can register a new account.
* [ ] AC-024: Registration validates required information.
* [ ] AC-025: A registered user can log in.
* [ ] AC-026: Invalid login credentials are rejected.
* [ ] AC-027: An authenticated user can log out.

### News

* [ ] AC-028: Users can view the news listing.
* [ ] AC-029: Users can open an individual news article.
* [ ] AC-030: News articles display title and content correctly.

### Static pages

* [ ] AC-031: About page is accessible.
* [ ] AC-032: Contact page is accessible.
* [ ] AC-033: Shipping policy page is accessible.
* [ ] AC-034: Privacy policy page is accessible.
* [ ] AC-035: Return/warranty policy page is accessible.
* [ ] AC-036: Terms of service page is accessible.
* [ ] AC-037: Shopping guide page is accessible.

### Quality

* [ ] AC-038: Backend unit tests cover core business logic.
* [ ] AC-039: Backend integration tests cover the main API flows.
* [ ] AC-040: Frontend tests cover the main user interactions.
* [ ] AC-041: End-to-end tests cover product browsing, product detail, cart and authentication flows.
* [ ] AC-042: The application can be built and run using Docker.
* [ ] AC-043: No critical console/runtime errors are present during the main user flows.
* [ ] AC-044: The implementation passes the defined SA code-review criteria.

## Constraints

### Technology

* Backend must use Java 21.
* Backend must use Spring Boot 4.
* Database must use PostgreSQL.
* Database migrations must use Flyway.
* Frontend must use React + TypeScript.
* Frontend should use the existing project standards defined in `project.md`.
* APIs must use REST/JSON.
* Use the existing repository architecture and coding standards.
* Do not introduce unnecessary infrastructure.

### Architecture

The SA must first analyze the reference website and create:

```text
docs/design/REQ-001-design.md
```

The design must define:

* Frontend architecture.
* Backend architecture.
* Database model.
* API design.
* Product/category model.
* Cart model.
* Authentication model.
* News model.
* Static content strategy.
* Image/asset strategy.
* Testing strategy.
* Deployment strategy.

### Performance

* Homepage should load efficiently.
* Product listing must avoid unnecessary API calls.
* Images must use appropriate dimensions/compression/lazy loading where applicable.
* Avoid unnecessary database queries.
* No advanced performance optimization is required beyond reasonable web application practices.

### Security

* Do not copy credentials, secrets, API keys, tracking IDs or private data from the reference website.
* Passwords must never be stored in plaintext.
* Authentication APIs must validate input.
* APIs must validate request parameters.
* Do not expose sensitive database information through API responses.

### Content / Assets

The reference website may be used as a visual and functional reference.

The implementation must not assume that all original website assets are free to copy.

Use:

* Newly created assets.
* Placeholder assets.
* Assets explicitly provided for the project.
* Assets with appropriate reuse rights.

Product data may be represented with synthetic/sample data where necessary.

### Compatibility

* Desktop browsers.
* Mobile browsers.
* Modern Chromium-based browsers.
* Safari.
* Responsive layouts.

### Deployment

The application must be able to run using:

```text
Docker
+
Application
+
PostgreSQL
```

## Notes

Reference website:

https://bietdoisanhang.vn/

The reference site is a Vietnamese e-commerce website for fishing bait and fishing equipment. It contains product categories, product detail pages, news, search, cart, authentication links, contact information and customer policy pages.

Examples of product information and product-detail behavior can be observed from the public product pages.

### Important SA instruction

The SA must NOT immediately start implementation.

First:

1. Inspect the reference website.
2. Identify page types.
3. Identify navigation structure.
4. Identify reusable UI components.
5. Identify functional flows.
6. Identify API requirements.
7. Identify data entities.
8. Identify dependencies.
9. Identify tasks.
10. Define technical acceptance criteria.
11. Create the architecture/design document.

Expected deliverables:

```text
docs/design/REQ-001-design.md

TASK-xxx Backend
TASK-xxx Frontend
TASK-xxx Database
TASK-xxx Test
TASK-xxx DevOps
```

The SA may modify the suggested task breakdown after analysis.

### Requirement change rule

Bumping `revision` while tasks exist:

```text
/scrum run
```

must BLOCK affected tasks with:

```text
reason: requirement_changed
```

until SA re-analyzes the requirement.

Do not silently continue against an outdated requirement revision.
