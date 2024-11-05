from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .models import Message, CustomUser
from .forms import UserRegistrationForm, UserProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration complete!")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "chat/register.html", {"form": form})

def chat_room(request, room_name):
    return render(request, 'chat/chat_room.html', {'room_name': room_name})

@login_required
def get_messages(request, recipient_id):
    recipient = get_object_or_404(CustomUser, id=recipient_id)
    sender = request.user
    messages = Message.objects.filter(sender=sender, recipient=recipient) | \
               Message.objects.filter(sender=recipient, recipient=sender)
    messages_data = [
        {
            "id": message.id,
            "sender_id": message.sender.id,
            "recipient_id": message.recipient.id,
            "content": message.get_content(),
            "timestamp": message.timestamp,
        }
        for message in messages.order_by('timestamp')
    ]
    return JsonResponse({"messages": messages_data})

@login_required
def profile_update(request):
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been successfully updated!")
            return redirect("profile_update")
    else:
        form = UserProfileUpdateForm(instance=request.user)
    return render(request, "chat/profile_update.html", {"form": form})