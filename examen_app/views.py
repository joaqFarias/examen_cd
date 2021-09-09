from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import User, Cita


@login_required
def index(request):
    if request.method == "POST":
        errors = Cita.objects.validador_basico(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

        else:
            cita_nueva = Cita.objects.create(
                autor=request.POST['autor'],
                contenido=request.POST['contenido'],
                #megustas=User.objects.filter(id=int(request.POST['user_id'])),
                num_megustas = 0,
                usuarios=User.objects.get(id=int(request.POST['user_id']))
            )
            cita_nueva.save()

            messages.success(request, "La cita se publico con exito.")


    all_citas = Cita.objects.all()
    citas_user = Cita.objects.filter(usuarios__id=int(request.session['user']['id']))

    context = {
        'user_id': request.session['user']['id'],
        'all_citas': all_citas,
        'citas_user': citas_user
    }
    
    return render(request, 'index.html', context)

@login_required
def edit(request, id):
    if request.method == "POST":
        user_edit = User.objects.get(id=int(id))

        errors = User.objects.validador_edit(request.POST, id=int(user_edit.id))

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            
            return redirect(f'/edit/user/{id}')
        else:
            request.session['user'] = {
                    "id" : user_edit.id,
                    "name": f"{request.POST['first_name']} {request.POST['last_name']}",
                    "email": request.POST['email'],
                }
                
            request.session['register_first_name'] =  request.POST['first_name']
            request.session['register_last_name'] =  request.POST['last_name']
            request.session['register_email'] =  request.POST['email']

            user_edit.first_name =  request.POST['first_name']
            user_edit.last_name =  request.POST['last_name']
            user_edit.email =  request.POST['email']
            user_edit.save()

            messages.success(request, "Los datos fueron modificados con exito.")

            return redirect('/')
    else:
        return render(request, 'edit.html')

@login_required
def user(request, id):

    all_citas = Cita.objects.filter(usuarios__id=int(id))
    user_cita = User.objects.get(id=int(id))

    context = {
        'user_id': request.session['user']['id'],
        'nombre_usuario': f'{user_cita.first_name} {user_cita.last_name}',
        'all_citas': all_citas
    }
    
    return render(request, 'user.html', context)

@login_required
def megusta(request, id, id_cita):
    
    cita_mg = Cita.objects.get(id=int(id_cita))

    
    all_usuarios = cita_mg.megustas.all()

    errors = {}
    for usuario in all_usuarios:
        if usuario == User.objects.get(id=int(id)):
            errors['mg'] = "Ya le ha dado MeGusta a esta cita";

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        cita_mg.megustas.add(User.objects.get(id=int(id)))
        cita_mg.num_megustas = int(cita_mg.num_megustas) +  1
        cita_mg.save()

        messages.success(request, "Ha dado MeGusta a la Cita.")

    return redirect('/')

@login_required
def borrar(request, id_cita):

    cita_borrar = Cita.objects.get(id=int(id_cita))
    cita_borrar.delete()

    messages.success(request, "La cita se elimino correctamente.")

    return redirect('/')