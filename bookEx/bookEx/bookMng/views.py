# 5/4
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import MainMenu, Book, Comment, Favorite, CartItem
from .forms import BookForm, CommentForm
from django.contrib.auth.models import User
from django.contrib import messages

def index(request):
    # grab all the books (or filter however you like)
    books = Book.objects.all()
    return render(request, 'bookMng/index.html', {
        'books': books,   # <-- this key must match your template’s for-loop
    })


def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  })


def displaybooks(request):
    q = request.GET.get('q', '').strip()  # Changed: capture search query (5/3)
    if q:
        books = Book.objects.filter(name__icontains=q)
    else:
        books = Book.objects.all()
    return render(request, 'bookMng/displaybooks.html', {
        'books': books,
        'search_query': q,
    })  # Changed: render displaybooks.html with books + query (5/3)



def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)

    book.pic_path = book.picture.url[14:]
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  })

from django.contrib.auth.decorators import login_required
from django.http import Http404

@login_required
def book_delete(request, book_id):
    try:
        book = Book.objects.get(id=book_id, username=request.user)
    except Book.DoesNotExist:
        raise Http404("Book not found or you do not have permission to delete it.")

    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('bookMng:mybooks')

    return render(request, 'bookMng/book_confirm_delete.html', {
        'book': book,
        'item_list': MainMenu.objects.all()
    })

def mybooks(request):
    books = Book.objects.all()
    return render(request, 'bookMng/mybooks.html', {'books': books})


def aboutus(request):
    return render(request, 'aboutus.html')

def search_books(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Book.objects.filter(Q(name__icontains=query))

    return render(request, 'search_results.html', {
        'query': query,
        'results': results,
    })
class Register(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Account created successfully for {username}!')
        return response

@login_required
def add_comment(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        Comment.objects.create(book=book, user=request.user, text=text)
        messages.success(request, 'Comment posted successfully!')
    return redirect(f'/mybooks/?book_id={book_id}&open_modal=true')

@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
    return redirect('mybooks')


@login_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)

    if created:
        messages.success(request, f'"{book.name}" added to favorites!')
    else:
        favorite.delete()
        messages.success(request, f'"{book.name}" removed from favorites.')

    return redirect('bookMng:mybooks')

from .models import Favorite

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'bookMng/favorites.html', {
        'favorites': favorites,
        'item_list': MainMenu.objects.all(),
    })
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'bookMng/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'item_list': MainMenu.objects.all()})

@login_required
def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'"{book.name}" added to your cart!')
    return redirect('cart')


@login_required
def update_cart(request, cart_item_id):
    if request.method == 'POST':
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        quantity = int(request.POST.get('quantity'))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('mybooks')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')