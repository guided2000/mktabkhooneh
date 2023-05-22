from django import template
from blog.models import post ,category
from django.utils import timezone
from django.utils.safestring import mark_safe


now = timezone.now()

register = template.Library()

@register.inclusion_tag('blog/latest-posts.html')
def latest_posts(arg=3):
    posts= post.objects.filter(status=1).order_by('-published_date')[:arg]
    return {'posts':posts}



@register.inclusion_tag('blog/category.html')
def post_categories():
    posts =post.objects.filter(status=1)
    categories =category.objects.all()
    cat_dict ={}
    for name in categories:
        cat_dict[name]=posts.filter(category=name).count()
    return {'categories':cat_dict}

@register.inclusion_tag('blog/list.html')
def title_list():
    posts= post.objects.filter(status=1).order_by('-published_date')
    return {'posts':posts}


@register.simple_tag
def post_index(post_id):
    post_list= post.objects.filter(status=1).filter(published_date__lte = now)
    id_list=[]
    
    for p in post_list:
        id_list.append(p.pk)
    res = [x for x in range(len(id_list)) if id_list[x] == int(post_id)]
    return int(res[0])

@register.simple_tag
def len_posts_list():
    posts_list= post.objects.filter(status=1).filter(published_date__lte = now)
    return int(len(posts_list))

    

@register.simple_tag
def page_list(post_id):
    post_list= post.objects.filter(status=1).filter(published_date__lte = now)
    id_list=[]
    title_list=[]
    image_list=[]
    for p in post_list:
            id_list.append(p.id)
            title_list.append(p.title)
            image_list.append(p.image.url)
    index =post_index(post_id)

    if index+1 == len_posts_list():
        nextpid =str(id_list[index-1])
        nexttitle =str(title_list[index-1])
        nextimage =str(image_list[index-1])
        
        button=''' <a href="#" style="max-width:50% " >                   
                    <div class="card mb-3" style="max-width: 540px;">
                      <div class="row g-0">
                        <div class="col-md-4">
                          <img src="{image}" class="img-fluid rounded-end" alt="...">
                        </div>
                        <div class="col-md-8">
                          <div class="card-body">
                            <h5 class="card-title">{title}</h5>
                            <p class="card-text">پست بعدی</p>
                          </div>
                        </div>
                      </div>
                    </div>	
                    </a>								
									  '''.replace("#" ,nextpid).replace("{title}" ,nexttitle).replace("{image}" ,nextimage)
        return mark_safe(button)


    elif 1<index+1 and index+1 < len_posts_list():
        nextpid =str(id_list[index-1])
        nexttitle =str(title_list[index-1])
        nextimage =str(image_list[index-1])
        pervid =str(id_list[index+1])
        pervtitle = str(title_list[index+1])
        pervimage= str(image_list[index+1])
        button='''<a href="#" style="max-width:50% ">          
                    <div class="card mb-3" style="max-width: 540px;">
                      <div class="row g-0">
                        <div class="col-md-4">
                          <img src="{image}" class="img-fluid rounded-end" alt="...">
                        </div>
                        <div class="col-md-8">
                          <div class="card-body">
                            <h5 class="card-title">{title}</h5>
                            <p class="card-text">پست بعدی</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </a>

                <a href="*" style="direction: ltr; max-width:50% ">
                    <div class="card mb-3" style="max-width: 540px; ">
                      <div class="row g-0">

                        <div class="col-md-8">
                          <div class="card-body">
                            <h5 class="card-title"  style="direction: ltr;">{title2}</h5>
                            <p class="card-text"  style="direction: ltr;">پست قبلی</p>
                          </div>
                        </div>

                        <div class="col-md-4">
                          <img src="{image2}" class="img-fluid rounded-start" alt="...">
                        </div>
                        
                      </div>
                    </div>

                </a> '''.replace("#" ,nextpid).replace("*",pervid).replace("{title}" ,nexttitle).replace("{image}" ,nextimage).replace("{title2}" ,pervtitle).replace("{image2}" ,pervimage)
        return mark_safe(button)


    elif index+1 == 1:
        pervid =str(id_list[index+1])
        pervtitle = str(title_list[index+1])
        pervimage= str(image_list[index+1])
        button='''<a href="#" style="direction: ltr; max-width:50%;margin-right:50%" >
                    <div class="card mb-3" style="max-width: 540px; ">
                      <div class="row g-0">

                        <div class="col-md-8">
                          <div class="card-body">
                            <h5 class="card-title"  style="direction: ltr;">{title2}</h5>
                            <p class="card-text"  style="direction: ltr;">پست قبلی</p>
                          </div>
                        </div>

                        <div class="col-md-4">
                          <img src="{image2}" class="img-fluid rounded-start" alt="...">
                        </div>
                        
                      </div>
                    </div>       
                    </a>'''.replace("#" ,pervid).replace("{title2}" ,pervtitle).replace("{image2}" ,pervimage)
        return mark_safe(button)

