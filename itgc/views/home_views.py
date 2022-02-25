import flask
from itgc.infrastructure.view_modifiers import response
from itgc.viewmodels.mission.mission_viewmodel import MissionViewModel
blueprint = flask.Blueprint('home', __name__, template_folder='templates')


@blueprint.route('/', methods=['GET'])
@response(template_file='/home/index.html')
def index_get():
    vm = MissionViewModel()
    return vm.to_dict()


@blueprint.route('/', methods=['POST'])
@response(template_file='/home/index.html')
def index_post():
    vm = MissionViewModel()
    vm.add_events()
    return vm.to_dict()

