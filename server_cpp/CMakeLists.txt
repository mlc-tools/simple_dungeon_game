project(project_lord)

cmake_minimum_required(VERSION 3.8)

set(server ${PROJECT_NAME}_server)

set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/../)

set(ROOT ${CMAKE_CURRENT_SOURCE_DIR})
include_directories(
	${ROOT}/
	${ROOT}/src/
	${ROOT}/src/ml/
	${ROOT}/mg/
	${ROOT}/external/
	/usr/local/include
)
link_directories(
	/usr/local/lib/
)

file(GLOB_RECURSE SRC src/*.cpp src/*.h external/*cpp external/*.h external/*.hpp)
file(GLOB_RECURSE MG mg/*.cpp mg/*.h)

add_definitions(-w -O2)
set(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} -std=c++14)

add_executable(server ${SRC} ${MG})
target_link_libraries(server event)

install(TARGETS server DESTINATION bin/server)