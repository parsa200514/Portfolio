from django.db.models import F
from django.shortcuts import render, redirect
from .models import Device, Brand
from .forms import DeviceForm, BrandSelectionForm
from django.http import JsonResponse, HttpResponse


def export_devices(request, task):
    if task == '1':
        devices = Brand.objects.filter(origin_country__iexact='Korea').values('name', 'origin_country')
        return JsonResponse(list(devices), safe=False)
    elif task == '2':
        if request.method == "POST":
            form = BrandSelectionForm(request.POST)
            if form.is_valid():
                selected_brand = form.cleaned_data['brand']
                devices = Device.objects.filter(brand=selected_brand).values('brand__name', 'model', 'color', 'price', 'display_size', 'in_stock', 'origin_country')
                return JsonResponse(list(devices), safe=False)
        else:
            form = BrandSelectionForm()
        return render(request, 'inventory_module/select_brand.html', {'form': form})
    elif task == '3':
        devices = Device.objects.filter(brand__origin_country__iexact=F('origin_country')).values('brand__name', 'model', 'color', 'price', 'display_size', 'in_stock', 'origin_country')
        return JsonResponse(list(devices), safe=False)
    else:
        return HttpResponse(status=404)







def device_list(request):
    devices = Device.objects.all()
    return render(request, 'inventory_module/device_list.html', {'devices': devices})


def add_device(request):
    if request.method == "POST":
        form = DeviceForm(request.POST)
        if form.is_valid():
            if Device.objects.filter(model=form.cleaned_data.get('model')).exists():
                form.add_error('model', 'We already have this model in our inventory')
            else:
                form.save()
                return redirect('device_list')
    else:
        form = DeviceForm()
    return render(request, 'inventory_module/add_device.html', {'form': form})
