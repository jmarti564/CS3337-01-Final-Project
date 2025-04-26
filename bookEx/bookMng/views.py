from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import MainMenu
from .forms import BookForm

from .models import Book

from .models import Comment

from django.http import HttpResponseRedirect

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseForbidden

def index(request):
    all_books  = Book.objects.order_by('-id')
    featured   = list(all_books[:8])
    more_books = list(all_books[8:16])

    for b in featured + more_books:
        parts = b.picture.name.split('static/', 1)
        b.static_path = parts[1] if len(parts) == 2 else b.picture.name

    return render(request, 'bookMng/index.html', {
        'item_list':  MainMenu.objects.all(),
        'featured':   featured,
        'more_books': more_books,
    })






def about(request):
    return render(request, 'bookMng/about.html')




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
                      'submitted': submitted,
                  })


def displaybooks(request):
    query = request.GET.get('q', '').strip()
    if query:
        books = Book.objects.filter(name__icontains=query)
    else:
        books = Book.objects.all()

    # recreate your pic_path if you need it:
    for b in books:
        parts = b.picture.name.split('static/', 1)
        b.static_path = parts[1] if len(parts) == 2 else b.picture.name

    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'query': query,
                  })

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # existing pic_path logic...
    parts = book.picture.name.split('static/', 1)
    book.static_path = parts[1] if len(parts) == 2 else book.picture.name

    # Handle comment submission
    if request.method == 'POST':
        text = request.POST.get('comment', '').strip()
        if text and request.user.is_authenticated:
            Comment.objects.create(
                book=book,
                user=request.user,
                text=text
            )
        # redirect to avoid resubmission on refresh
        return redirect('book_detail', book_id=book.id)

    # Fetch all comments for this book, newest first
    comments = book.comments.order_by('-created_at')

    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'comments': comments,
                  })

def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user == book.username or request.user.is_superuser:
        book.delete()
        # look for a ?next=… param
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('displaybooks')
    return HttpResponseForbidden("You don’t have permission to delete this book.")

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Only the comment owner or a superuser may delete
    if comment.user == request.user or request.user.is_superuser:
        book_id = comment.book.id
        comment.delete()
        return redirect('book_detail', book_id=book_id)
    return HttpResponseForbidden("You don’t have permission to delete this comment.")


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

def mybooks(request):
    if request.user.is_authenticated: #If user is logged in
        books = Book.objects.filter(username=request.user)
        for b in books:
            b.pic_path = b.picture.url.split('static/', 1)[-1]
    else: #show user an empty page
        books = []
    return render(request, 'bookMng/mybooks.html', {
        'item_list': MainMenu.objects.all(),
        'books':     books,
    })

