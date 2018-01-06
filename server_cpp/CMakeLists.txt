project(server_cpp)

cmake_minimum_required(VERSION 3.7)

set(server ${PROJECT_NAME}_server)

set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/)

set(ROOT ${CMAKE_CURRENT_SOURCE_DIR})
include_directories(
	${ROOT}/
	${ROOT}/src/
	${ROOT}/src/ml/
	${ROOT}/mg/
	${ROOT}/external/
)
link_directories(
	/usr/local/lib/
)

if(WIN32)
    include_directories(
        ${ROOT}/external/libevent/include
        ${ROOT}/external/libevent/include/WIN32-Code/nmake
    )
    link_directories(
        ${ROOT}/external/libevent/lib
    )
else()
    include_directories(
        /usr/local/include
    )
    link_directories(
        /usr/local/lib/
    )
endif()

file(GLOB_RECURSE SRC src/*.cpp src/*.h external/*cpp external/*.h external/*.hpp)
file(GLOB_RECURSE MG mg/*.cpp mg/*.h)

set(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} -std=c++14)

add_executable(server ${SRC} ${MG})
target_link_libraries(server event)

install(TARGETS server DESTINATION bin)
